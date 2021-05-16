from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.dateparse import parse_date

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

import csv

from profiles.models import Profile
from .utils import get_report_image
from .models import Report
from sales.models import Sale, Position, CSV
from products.models import Product
from customers.models import Customer

# Create your views here.

class ReportListView(ListView):
    model = Report
    template_name = 'reports/main.html'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'

class UploadTemplateView(TemplateView):
    template_name = 'reports/from_file.html'

def csv_upload_view(request):
    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)
        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, 'r') as f:
                reader = CSV.reader(f)
                reader.__next__()
                for row in reader:
                    # print(row, type(row))
                    data = "".join(row).split(';')
                    data.pop()
                    #(_, transaction_id, product, quantity, customer, date, *rest) = data
                    (_, transaction_id, product, quantity, customer, date) = data
                    quantity = int(quantity)
                    date = parse_date(date)
                    try:
                        product.obj = Product.objects.get(name__iexact=product)
                    except ProductDoesNotExist:
                        product_obj = None
                        #
                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Positision.objects.create(product=product_obj,
                                                                 quantity=quantity,
                                                                 created_at=date)
                        sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id,
                                                                 customer=customer_obj,
                                                                 salesman=salesman_obj,
                                                                 created_at=date)
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()
    #
    return HttpResponse()

def create_report_view(request):
    if request.is_ajax():
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')
        img = get_report_image(image)
        author = Profile.objects.get(user=request.user)
        Report.objects.create(name=name, remarks=remarks, image=img, author=author)
        return JsonResponse({'msg': 'Send'})
    #
    return JsonResponse({})

def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response)

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
