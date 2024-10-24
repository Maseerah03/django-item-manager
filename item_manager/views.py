import csv
from django.shortcuts import render
from .forms import UploadCSVForm
from .forms import SearchForm
from .models import Item

def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                Item.objects.create(
                    item_name=row['Item Name'],
                    item_description=row['Item Description'],
                    item_code=row['Item Code'],
                    item_qty=row['Item Qty'],
                    item_price=row['Item Price'],
                    vendor_name=row['Vendor Name']
                )

            return render(request, 'upload_success.html')
    else:
        form = UploadCSVForm()

    return render(request, 'upload_csv.html', {'form': form})

from django.db.models import Q

def search_items(request):
    form = SearchForm(request.GET or None)
    items = Item.objects.all()

    if form.is_valid():
        item_name = form.cleaned_data.get('item_name')
        item_code = form.cleaned_data.get('item_code')
        vendor_name = form.cleaned_data.get('vendor_name')

        if item_name:
            items = items.filter(item_name__icontains=item_name)
        if item_code:
            items = items.filter(item_code__icontains=item_code)
        if vendor_name:
            items = items.filter(vendor_name__icontains=vendor_name)

    return render(request, 'search_items.html', {'form': form, 'items': items})

from reportlab.pdfgen import canvas
from django.http import HttpResponse

def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="items.pdf"'

    p = canvas.Canvas(response)

    items = Item.objects.all()
    y = 800  # Start from the top of the page
    for item in items:
        p.drawString(100, y, f"{item.item_name} | {item.item_code} | {item.vendor_name} | {item.item_qty} | {item.item_price}")
        y -= 20  # Move down the page

    p.showPage()
    p.save()
    return response

import openpyxl
from django.http import HttpResponse

def export_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=items.xlsx'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Items'

    # Header
    ws.append(['Item Name', 'Item Code', 'Vendor Name', 'Item Qty', 'Item Price'])

    # Data
    items = Item.objects.all()
    for item in items:
        ws.append([item.item_name, item.item_code, item.vendor_name, item.item_qty, item.item_price])

    wb.save(response)
    return response
