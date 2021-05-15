from django.shortcuts import render
from django.views.generic import ListView, DetailView
import pandas as pd

from .models import Sale
from .forms import SalesSearchForm


# Create your views here.
def home_view(request):
    ## function views
    form = SalesSearchForm(request.POST or None)
    sales_df, position_df = None, None

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')

        sales_qs = Sale.objects.filter(created_at__date__lte=date_to,
                                      created_at__date__gte=date_from) # queryset
        if len(sales_qs) > 0:
            sales_df = pd.DataFrame(sales_qs.values()).to_html()
            position_data = [
                {
                    'position_id': pos.id,
                    'product': pos.product.name,
                    'quantity': pos.quantity,
                    'price': pos.price
                } for sale in sales_qs for pos in sale.get_positions()
            ]
            position_df = pd.DataFrame(position_data).to_html()
        else:
            print("No data")

    ctxt = {
        'form': form,
        'sales_df': sales_df,
        'position_df': position_df,
    }
    return render(request, 'sales/home.html', ctxt)

class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'
    # context_object_name = 'qs' would replace object_list in the view main.html

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'
