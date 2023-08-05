import csv
import codecs
import logging
import os
import sys
import uuid

from .settings import MEDIA_URL
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template.response import TemplateResponse
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.urls import reverse
from django.utils.encoding import smart_str
from django.contrib import messages

from json import loads, dumps
from math import ceil

from .convert import full_part_number_to_broken_part
from .models import Part, PartClass, Subpart, SellerPart, Organization, PartFile, Manufacturer
from .forms import PartInfoForm, PartForm, AddSubpartForm, FileForm, AddSellerPartForm
from .octopart_parts_match import match_part

logger = logging.getLogger(__name__)


@login_required
def home(request):
    profile = request.user.bom_profile()
    organization = profile.organization

    if profile.organization is None:
        organization, created = Organization.objects.get_or_create(
            owner=request.user,
            defaults={'name': request.user.first_name + ' ' + request.user.last_name,
                      'subscription': 'F'},
        )

        profile.organization = organization
        profile.role = 'A'
        profile.save()

    parts = Part.objects.filter(
        organization=organization).order_by(
        'number_class__code',
        'number_item',
        'number_variation')

    autocomplete_dict = {}
    for part in parts:
        if part.description:
            autocomplete_dict.update({ part.description.replace('"', ''): None })
        # autocomplete_dict.update({ part.full_part_number(): None }) # TODO: query full part number
        if part.manufacturer_part_number:
            autocomplete_dict.update({ part.manufacturer_part_number.replace('"', ''): None })
        if part.manufacturer is not None and part.manufacturer.name:
            autocomplete_dict.update({ part.manufacturer.name.replace('"', ''): None })

    autocomplete = dumps(autocomplete_dict)

    def numbers_from_part_string(s):
        number_class = None
        number_item = None
        number_variation = None

        if len(s) >= 3:
            number_class = s[:3]
            if len(s) >= 8 and s[3] == '-':
                number_item = s[4:8]
                if len(s) >= 10 and s[8] == '-':
                    number_variation = s[9:]

        return (number_class, number_item, number_variation)

    query = request.GET.get('q', '')
    if query:
        rq = query.strip()
        (number_class, number_item, number_variation) = numbers_from_part_string(rq)
        if number_class and number_item and number_variation:
            parts = parts.filter(
                Q(number_class__code=number_class, number_item=number_item, number_variation=number_variation) | 
                Q(description__icontains=query) | 
                Q(manufacturer_part_number__icontains=query) | 
                Q(manufacturer__name__icontains=query))
        elif number_class and number_item:
            parts = parts.filter(
                Q(number_class__code=number_class, number_item=number_item) | 
                Q(description__icontains=query) | 
                Q(manufacturer_part_number__icontains=query) | 
                Q(manufacturer__name__icontains=query))
        else:
            parts = parts.filter(
                Q(description__icontains=query) | 
                Q(manufacturer_part_number__icontains=query) | 
                Q(manufacturer__name__icontains=query) |
                Q(number_class__code=query))
    
    return TemplateResponse(request, 'bom/dashboard.html', locals())


def error(request):
    msgs = messages.get_messages(request)
    return TemplateResponse(request, 'bom/error.html', locals())


@login_required
def bom_signup(request):
    user = request.user
    organization = user.bom_profile().organization

    if organization is not None:
        return HttpResponseRedirect(reverse('bom:home'))

    return TemplateResponse(request, 'bom/bom-signup.html', locals())


@login_required
def part_info(request, part_id):
    order_by = request.GET.get('order_by', 'indented')
    anchor = None

    user = request.user
    profile = user.bom_profile()
    organization = profile.organization

    try:
        part = Part.objects.get(id=part_id)
    except ObjectDoesNotExist:
        messages.error(request, "Part object does not exist.")
        return HttpResponseRedirect(reverse('bom:error'))

    if part.organization != organization:
        messages.error(request, "Cant access a part that is not yours!")
        return HttpResponseRedirect(reverse('bom:error'))

    qty_cache_key = str(part_id) + '_qty'
    qty = cache.get(qty_cache_key, 100)
    part_info_form = PartInfoForm(initial={'quantity': qty})
    upload_file_to_part_form = FileForm()

    if request.method == 'POST':
        part_info_form = PartInfoForm(request.POST)
        if part_info_form.is_valid():
            qty = request.POST.get('quantity', 100)
    
    cache.set(qty_cache_key, qty, 3600)
    
    try:
        parts = part.indented()
    except RuntimeError:
        messages.error(request, "Error: infinite recursion in part relationship. Contact info@indabom.com to resolve.")
        parts = []

    extended_cost_complete = True
    unit_cost = 0
    unit_nre = 0
    unit_out_of_pocket_cost = 0
    for item in parts:
        extended_quantity = int(qty) * item['quantity']
        item['extended_quantity'] = extended_quantity

        subpart = item['part']
        seller = subpart.optimal_seller(quantity=extended_quantity)
        order_qty = extended_quantity
        if seller is not None and seller.minimum_order_quantity is not None and extended_quantity > seller.minimum_order_quantity:
            order_qty = ceil(extended_quantity / float(seller.minimum_order_quantity)) * seller.minimum_order_quantity

        item['seller_price'] = seller.unit_cost if seller is not None else 0
        item['seller_nre'] = seller.nre_cost if seller is not None else 0
        item['seller_part'] = seller
        item['seller_moq'] = seller.minimum_order_quantity if seller is not None else 0
        item['order_quantity'] = order_qty

        # then extend that price
        item['extended_cost'] = extended_quantity * \
            seller.unit_cost if seller is not None and seller.unit_cost is not None and extended_quantity is not None else None
        item['out_of_pocket_cost'] = order_qty * \
            float(seller.unit_cost) if seller is not None and seller.unit_cost is not None else 0

        unit_cost = (
            unit_cost +
            seller.unit_cost *
            item['quantity']) if seller is not None and seller.unit_cost is not None else unit_cost
        unit_out_of_pocket_cost = unit_out_of_pocket_cost + \
            item['out_of_pocket_cost']
        unit_nre = (
            unit_nre +
            item['seller_nre']) if item['seller_nre'] is not None else unit_nre
        if seller is None:
            extended_cost_complete = False

    # seller_price, seller_nre

    extended_cost = unit_cost * int(qty)
    total_out_of_pocket_cost = unit_out_of_pocket_cost + float(unit_nre)

    where_used = part.where_used()
    files = part.files()
    seller_parts = part.seller_parts()

    if order_by != 'defaultOrderField' and order_by != 'indented':
        anchor = 'bom'
        parts = sorted(parts, key=lambda k: k[order_by], reverse=True)
    elif order_by == 'indented':
        anchor = 'bom'

    return TemplateResponse(request, 'bom/part-info.html', locals())


@login_required
def part_export_bom(request, part_id):
    user = request.user
    profile = user.bom_profile()
    organization = profile.organization

    try:
        part = Part.objects.get(id=part_id)
    except ObjectDoesNotExist:
        messages.error(request, "Part object does not exist.")
        return HttpResponseRedirect(reverse('bom:error'))

    if part.organization != organization:
        messages.error(request, "Cant export a part that is not yours!")
        return HttpResponseRedirect(reverse('bom:error'))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}_indabom_parts_indented.csv"'.format(part.full_part_number())

    bom = part.indented()
    qty_cache_key = str(part_id) + '_qty'
    qty = cache.get(qty_cache_key, 1000)
    unit_cost = 0
    unit_out_of_pocket_cost = 0
    unit_nre = 0

    fieldnames = [
        'level',
        'part_number',
        'quantity',
        'part_description',
        'part_revision',
        'part_manufacturer',
        'part_manufacturer_part_number',
        'part_ext_qty',
        'part_order_qty',
        'part_seller',
        'part_cost',
        'part_moq',
        'part_ext_cost',
        'part_out_of_pocket_cost',
        'part_nre',
        'part_lead_time_days', ]

    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    for item in bom:
        extended_quantity = int(qty) * item['quantity']
        item['extended_quantity'] = extended_quantity

        subpart = item['part']
        seller = subpart.optimal_seller(quantity=extended_quantity)
        order_qty = extended_quantity
        if seller is not None and seller.minimum_order_quantity is not None and extended_quantity > seller.minimum_order_quantity:
            order_qty = ceil(extended_quantity / float(seller.minimum_order_quantity)) * seller.minimum_order_quantity

        item['seller_price'] = seller.unit_cost if seller is not None else 0
        item['seller_nre'] = seller.nre_cost if seller is not None else 0
        item['seller_part'] = seller
        item['seller_moq'] = seller.minimum_order_quantity if seller is not None else 0
        item['order_quantity'] = order_qty
        item['seller_lead_time_days'] = seller.lead_time_days if seller is not None else 0

        # then extend that price
        item['extended_cost'] = extended_quantity * \
            seller.unit_cost if seller is not None and seller.unit_cost is not None and extended_quantity is not None else None
        item['out_of_pocket_cost'] = order_qty * \
            float(seller.unit_cost) if seller is not None and seller.unit_cost is not None else 0

        unit_cost = (
            unit_cost +
            seller.unit_cost *
            item['quantity']) if seller is not None and seller.unit_cost is not None else unit_cost
        unit_out_of_pocket_cost = unit_out_of_pocket_cost + \
            item['out_of_pocket_cost']
        unit_nre = (
            unit_nre +
            item['seller_nre']) if item['seller_nre'] is not None else unit_nre
        if seller is None:
            extended_cost_complete = False

        row = {
            'level': item['indent_level'],
            'part_number': item['part'].full_part_number(),
            'quantity': item['quantity'],
            'part_description': item['part'].description,
            'part_revision': item['part'].revision,
            'part_manufacturer': item['part'].manufacturer.name if item['part'].manufacturer is not None else '',
            'part_manufacturer_part_number': item['part'].manufacturer_part_number,
            'part_ext_qty': item['extended_quantity'],
            'part_order_qty': item['order_quantity'],
            'part_seller': item['seller_part'].seller.name if item['seller_part'] is not None else '',
            'part_cost': item['seller_price'] if item['seller_price'] is not None else 0,
            'part_moq': item['seller_moq'] if item['seller_moq'] is not None else 0,
            'part_ext_cost': item['extended_cost'] if item['extended_cost'] is not None else 0,
            'part_out_of_pocket_cost': item['out_of_pocket_cost'],
            'part_nre': item['seller_nre'] if item['seller_nre'] is not None else 0,
            'part_lead_time_days': item['seller_lead_time_days'], 
        }
        writer.writerow({k:smart_str(v) for k,v in row.items()})
    return response


@login_required
def part_upload_bom(request, part_id):
    try:
        part = Part.objects.get(id=part_id)
    except ObjectDoesNotExist:
        messages.error(request, "No part found with given part_id.")
        return HttpResponseRedirect(reverse('bom:error'))

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            csvfile = request.FILES['file']
            # dialect = csv.Sniffer().sniff(csvfile.readline())
            csvfile.open()
            reader = csv.reader(codecs.iterdecode(csvfile, 'utf-8'))
            headers = [h.lower() for h in next(reader)]
            # Subpart.objects.filter(assembly_part=part).delete()

            header_error = False
            if 'part_number' not in headers and 'manufacturer_part_number' not in headers:
                header_error = True
                messages.error(request, "Header `part_number` or `manufacturer_part_number` required for upload.")
            if 'quantity' not in headers:
                header_error = True
                messages.error(request, "Header `quantity` required for upload.")

            if header_error:
                return HttpResponseRedirect(reverse('bom:part-manage-bom', kwargs={'part_id': part_id}))

            for row in reader:
                partData = {}
                for idx, item in enumerate(row):
                    partData[headers[idx]] = item
                
                if 'part_number' in partData and 'quantity' in partData and len(partData['part_number']) > 0:
                    try:
                        civ = full_part_number_to_broken_part(
                            partData['part_number'])
                        subparts = Part.objects.filter(
                            number_class=civ['class'],
                            number_item=civ['item'],
                            number_variation=civ['variation'])
                    except IndexError:
                        messages.error(
                            request, "Invalid part_number: {}".format(partData['part_number']))
                        continue

                    if len(subparts) == 0:
                        messages.info(
                            request, "Subpart: `{}` doesn't exist".format(
                                partData['part_number']))
                        continue

                    subpart = subparts[0]
                    count = partData['quantity']
                    if part == subpart:
                        messages.error(
                            request, "Recursive part association: a part cant be a subpart of itsself")
                        return HttpResponseRedirect(reverse('bom:part-manage-bom', kwargs={'part_id': part_id}))

                    sp = Subpart(
                        assembly_part=part,
                        assembly_subpart=subpart,
                        count=count)
                    sp.save()
                elif 'manufacturer_part_number' in partData and 'quantity' in partData:
                    mpn = partData['manufacturer_part_number']
                    subparts = Part.objects.filter(manufacturer_part_number=mpn)

                    if len(subparts) == 0:
                        messages.info(
                            request, "Subpart: `{}` doesn't exist".format(
                                partData['manufacturer_part_number']))
                        continue

                    subpart = subparts[0]
                    count = partData['quantity']
                    if part == subpart:
                        messages.error(
                            request, "Recursive part association: a part cant be a subpart of itsself")
                        return HttpResponseRedirect(reverse('bom:part-manage-bom', kwargs={'part_id': part_id}))

                    sp = Subpart(
                        assembly_part=part,
                        assembly_subpart=subpart,
                        count=count)
                    sp.save()
        else:
            messages.error(
                request,
                "File form not valid: {}".format(
                    form.errors))
            return HttpResponseRedirect(reverse('bom:part-manage-bom', kwargs={'part_id': part_id}))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('bom:home')))


@login_required
def upload_parts(request):
    user = request.user
    profile = user.bom_profile()
    organization = profile.organization
    partclasses = PartClass.objects.all()

    if request.method == 'POST' and request.FILES['file'] is not None:
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            csvfile = request.FILES['file']
            # dialect = csv.Sniffer().sniff(csvfile.readline())
            csvfile.open()
            reader = csv.reader(codecs.iterdecode(csvfile, 'utf-8'))
            headers = [h.lower() for h in next(reader)]
            for row in reader:
                partData = {}
                for idx, item in enumerate(row):
                    partData[headers[idx]] = item
                if 'part_class' in partData and 'description' in partData and 'revision' in partData:
                    mpn = ''
                    mfg = None
                    if 'manufacturer_part_number' in partData:
                        mpn = partData['manufacturer_part_number']
                    if 'manufacturer' in partData:
                        mfg_name = partData['manufacturer'] if partData['manufacturer'] is not None else ''
                        mfg, created = Manufacturer.objects.get_or_create(
                            name=mfg_name, organization=organization)

                    try:
                        part_class = PartClass.objects.get(
                            code=partData['part_class'])
                    except PartClass.DoesNotExist:
                        messages.error(
                            request, "Partclass {} doesn't exist.".format(
                                partData['part_class']))
                        return HttpResponseRedirect(reverse('bom:error'))

                    part, created = Part.objects.get_or_create(number_class=part_class,
                                                               organization=organization,
                                                               manufacturer_part_number=mpn,
                                                               manufacturer=mfg,
                                                               defaults={
                                                                   'description': partData['description'],
                                                                   'revision': partData['revision'],
                                                               })
                    if created:
                        messages.info(
                            request, "{}: {} created.".format(
                                part.full_part_number(), part.description))
                    else:
                        messages.warning(
                            request, "{}: {} already exists!".format(
                                part.full_part_number(), part.description))
                else:
                    messages.error(
                        request,
                        "File must contain at least the 3 columns (with headers): 'part_class', 'description', and 'revision'.")
                    return TemplateResponse(request, 'bom/upload-parts.html', locals())
        else:
            messages.error(request, "Invalid form input.")
            return TemplateResponse(request, 'bom/upload-parts.html', locals())
    else:
        form = FileForm()
        return TemplateResponse(request, 'bom/upload-parts.html', locals())

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('bom:home')))


@login_required
def export_part_list(request):
    user = request.user
    profile = user.bom_profile()
    organization = profile.organization

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="indabom_parts.csv"'

    parts = Part.objects.filter(
        organization=organization).order_by(
        'number_class__code',
        'number_item',
        'number_variation')

    fieldnames = [
        'part_number',
        'part_description',
        'part_revision',
        'part_manufacturer',
        'part_manufacturer_part_number',
    ]

    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    for item in parts:
        row = {
            'part_number': item.full_part_number(),
            'part_description': item.description,
            'part_revision': item.revision,
            'part_manufacturer': item.manufacturer.name if item.manufacturer is not None else '',
            'part_manufacturer_part_number': item.manufacturer_part_number if item.manufacturer is not None else '',
        }
        writer.writerow({k:smart_str(v) for k,v in row.items()})

    return response


@login_required
def part_octopart_match(request, part_id):
    try:
        part = Part.objects.get(id=part_id)
    except ObjectDoesNotExist:
        messages.error(request, "No part found with given part_id.")
        return HttpResponseRedirect(reverse('bom:error'))

    seller_parts = []
    try:
        seller_parts = match_part(part, request.user.bom_profile().organization)
    except IOError as e:
        messages.error(request, "Error communicating with Octopart. {}".format(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('bom:home')) + '#sourcing')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        messages.error(request, "Error - {}: {}, ({}, {})".format(exc_type, e, fname, exc_tb.tb_lineno))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('bom:home')) + '#sourcing')

    if len(seller_parts) > 0:
        for dp in seller_parts:
            try:
                dp.save()
            except IntegrityError:
                continue
    else:
        messages.info(
            request,
            "Octopart wasn't able to find any parts with manufacturer part number: {}".format(
                part.manufacturer_part_number))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('bom:home')) + '#sourcing')


@login_required
def part_octopart_match_bom(request, part_id):
    try:
        part = Part.objects.get(id=part_id)
    except ObjectDoesNotExist:
        messages.error(request, "No part found with given part_id.")
        return HttpResponseRedirect(reverse('bom:error'))

    subparts = part.subparts.all()
    seller_parts = []

    for part in subparts:
        try:
            seller_parts = match_part(part, request.user.bom_profile().organization)
        except IOError as e:
            messages.error(request, "Error communicating with Octopart.")
            continue
        except Exception as e:
            messages.error(request, "Unknown Error: {}".format(e))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('bom:home')) + '#sourcing')

        if len(seller_parts) > 0:
            for sp in seller_parts:
                try:
                    sp.save()
                except IntegrityError:
                    continue
        else:
            messages.info(
                request,
                "Octopart wasn't able to find any parts with manufacturer part number: {}".format(
                    part.manufacturer_part_number))
            continue

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('bom:home')))


@login_required
def create_part(request):
    user = request.user
    profile = user.bom_profile()
    organization = profile.organization

    if request.method == 'POST':
        form = PartForm(request.POST, organization=organization)
        if form.is_valid():
            try:
                new_part, created = Part.objects.get_or_create(
                    number_class=form.cleaned_data['number_class'],
                    number_item=form.cleaned_data['number_item'],
                    number_variation=form.cleaned_data['number_variation'],
                    manufacturer_part_number=form.cleaned_data['manufacturer_part_number'],
                    manufacturer=form.cleaned_data['manufacturer'],
                    organization=organization,
                    defaults={'description': form.cleaned_data['description'],
                            'revision': form.cleaned_data['revision'],
                            }
                )
            except IntegrityError as e:
                messages.error(request, "Error creating part, please contact info@indabom.com with this information: {}".format(e))
            
            if not new_part.manufacturer_part_number:
                new_part.manufacturer_part_number = new_part.full_part_number()
                new_part.save()
            
            return HttpResponseRedirect(
                reverse('bom:part-info',
                    kwargs={'part_id': str(new_part.id)}))
    else:
        form = PartForm(organization=organization)

    return TemplateResponse(request, 'bom/create-part.html', locals())


@login_required
def part_edit(request, part_id):
    user = request.user
    profile = user.bom_profile()
    organization = profile.organization

    try:
        part = Part.objects.get(id=part_id)
    except ObjectDoesNotExist:
        messages.error(request, "No part found with given part_id.")
        return HttpResponseRedirect(reverse('bom:error'))

    if request.method == 'POST':
        form = PartForm(request.POST, organization=organization)
        if form.is_valid():
            old_part = Part.objects.get(id=part_id)

            old_part.number_class = form.cleaned_data['number_class']
            old_part.number_item = form.cleaned_data['number_item']
            old_part.number_variation = form.cleaned_data['number_variation']
            old_part.manufacturer_part_number = form.cleaned_data['manufacturer_part_number']
            old_part.manufacturer = form.cleaned_data['manufacturer']
            old_part.description = form.cleaned_data['description']
            old_part.revision = form.cleaned_data['revision']
            old_part.save()

            return HttpResponseRedirect(
                reverse(
                    'bom:part-info',
                    kwargs={
                        'part_id': part_id}))
    else:
        form = PartForm(
            initial={
                'number_class': part.number_class,
                'number_item': part.number_item,
                'number_variation': part.number_variation,
                'description': part.description,
                'revision': part.revision,
                'manufacturer_part_number': part.manufacturer_part_number,
                'manufacturer': part.manufacturer,
            },
            organization=organization)

    return TemplateResponse(request, 'bom/edit-part.html', locals())


@login_required
def manage_bom(request, part_id):
    user = request.user
    profile = user.bom_profile()
    organization = profile.organization

    try:
        part = Part.objects.get(id=part_id)
    except ObjectDoesNotExist:
        messages.error(request, "Part object does not exist.")
        return HttpResponseRedirect(reverse('bom:error'))

    if part.organization != organization:
        messages.error(request, "Cant access a part that is not yours!")
        return HttpResponseRedirect(reverse('bom:error'))

    add_subpart_form = AddSubpartForm(
        initial={'count': 1, }, organization=organization, part_id=part_id)
    upload_subparts_csv_form = FileForm()

    parts = part.indented()
    for item in parts:
        extended_quantity = 1000 * item['quantity']
        seller = item['part'].optimal_seller(quantity=extended_quantity)
        item['seller_price'] = seller.unit_cost if seller is not None else None
        item['seller_part'] = seller

    return TemplateResponse(request, 'bom/manage-bom.html', locals())


@login_required
def part_delete(request, part_id):
    try:
        part = Part.objects.get(id=part_id)
    except ObjectDoesNotExist:
        messages.error(request, "No part found with given part_id.")
        return HttpResponseRedirect(reverse('bom:error'))

    part.delete()

    return HttpResponseRedirect(reverse('bom:home'))


@login_required
def add_subpart(request, part_id):
    user = request.user
    profile = user.bom_profile()
    organization = profile.organization

    try:
        part = Part.objects.get(id=part_id)
    except ObjectDoesNotExist:
        messages.error(request, "No part found with given part_id.")
        return HttpResponseRedirect(reverse('bom:error'))

    if request.method == 'POST':
        form = AddSubpartForm(request.POST, organization=organization, part_id=part_id)
        if form.is_valid():
            new_part = Subpart.objects.create(
                assembly_part=part,
                assembly_subpart=form.cleaned_data['assembly_subpart'],
                count=form.cleaned_data['count']
            )

    return HttpResponseRedirect(reverse('bom:part-info', kwargs={'part_id': part_id}) + '#bom')


@login_required
def remove_subpart(request, part_id, subpart_id):
    try:
        subpart = Subpart.objects.get(id=subpart_id)
    except ObjectDoesNotExist:
        messages.error(request, "No subpart found with given part_id.")
        return HttpResponseRedirect(reverse('bom:part-info', kwargs={'part_id': part_id}) + '#bom')

    subpart.delete()

    return HttpResponseRedirect(reverse('bom:part-manage-bom', kwargs={'part_id': part_id}))


@login_required
def remove_all_subparts(request, part_id):
    subparts = Subpart.objects.filter(assembly_part=part_id)

    for subpart in subparts:
        subpart.delete()

    return HttpResponseRedirect(reverse('bom:part-manage-bom', kwargs={'part_id': part_id}))


@login_required
def upload_file_to_part(request, part_id):
    try:
        part = Part.objects.get(id=part_id)
    except ObjectDoesNotExist:
        messages.error(request, "No part found with given part_id.")
        return HttpResponseRedirect(reverse('bom:error'))

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            partfile = PartFile(file=request.FILES['file'], part=part)
            partfile.save()
            return HttpResponseRedirect(reverse('bom:part-info', kwargs={'part_id': part_id}) + '#specs')

    messages.error(request, "Error uploading file.")
    return HttpResponseRedirect(reverse('bom:error'))


@login_required
def delete_file_from_part(request, part_id, partfile_id):
    try:
        partfile = PartFile.objects.get(id=partfile_id)
    except ObjectDoesNotExist:
        messages.error(request, "No file found with given file id.")
        return HttpResponseRedirect(reverse('bom:error'))

    partfile.delete()

    return HttpResponseRedirect(reverse('bom:part-info', kwargs={'part_id': part_id}) + '#specs')


@login_required
def add_sellerpart(request, part_id):
    user = request.user
    profile = user.bom_profile()
    organization = profile.organization

    try:
        part = Part.objects.get(id=part_id)
    except ObjectDoesNotExist:
        messages.error(request, "No part found with given part_id.")
        return HttpResponseRedirect(reverse('bom:error'))

    if request.method == 'POST':
        form = AddSellerPartForm(request.POST, organization=organization)
        if form.is_valid():
            new_sellerpart, created = SellerPart.objects.get_or_create(
                part=part,
                seller=form.cleaned_data['seller'],
                minimum_order_quantity=form.cleaned_data['minimum_order_quantity'],
                minimum_pack_quantity=form.cleaned_data['minimum_pack_quantity'],
                unit_cost=form.cleaned_data['unit_cost'],
                lead_time_days=form.cleaned_data['lead_time_days'],
                nre_cost=form.cleaned_data['nre_cost'],
                ncnr=form.cleaned_data['ncnr'],
            )
        else:
            messages.error(request,"Form not valid. See error(s) below.")
            return TemplateResponse(request, 'bom/add-sellerpart.html', locals())
    else:
        if part.organization != organization:
            messages.error(request, "Cant access a part that is not yours!")
            return HttpResponseRedirect(reverse('bom:error'))
        form = AddSellerPartForm(organization=organization)
        return TemplateResponse(request, 'bom/add-sellerpart.html', locals())

    return HttpResponseRedirect(reverse('bom:part-info', kwargs={'part_id': part_id}) + '#sourcing')


@login_required
def delete_sellerpart(request, sellerpart_id):
    # TODO: Add test
    try:
        sellerpart = SellerPart.objects.get(id=sellerpart_id)
    except ObjectDoesNotExist:
        messages.error(request, "No sellerpart found with given sellerpart_id.")
        return HttpResponseRedirect(reverse('bom:error'))

    sellerpart.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('bom:home')))
