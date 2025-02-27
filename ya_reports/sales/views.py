from django.shortcuts import render
from django.views.generic import ListView, DetailView
import pandas as pd

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Sale
from reports.forms import ReportForm
from .forms import SalesSearchForm
from .utils import get_salesman_from_id, get_customer_from_id, get_chart


# Create your views here.
@login_required
def home_view(request):
    ## function views
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()
    sales_df, position_df, merged_df, gdf = None, None, None, None
    chart = None
    no_data = None

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        result_by = request.POST.get('results_by')
        sales_qs = Sale.objects.filter(created_at__date__lte=date_to,
                                      created_at__date__gte=date_from) # queryset
        if len(sales_qs) > 0:
            sales_df = pd.DataFrame(sales_qs.values())
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman',
                             'id': 'sales_id'}, axis=1, inplace=True)
            sales_df['created_at'] = sales_df['created_at'].apply(lambda dt: dt.strftime("%d-%m-%Y"))
            position_data = [
                {
                    'position_id': pos.id,
                    'product': pos.product.name,
                    'quantity': pos.quantity,
                    'price': pos.price,
                    'sales_id': pos.get_sales_id(),
                } for sale in sales_qs for pos in sale.get_positions()
            ]
            position_df = pd.DataFrame(position_data)
            merged_df = pd.merge(sales_df, position_df, on='sales_id')
            gdf = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')
            chart = get_chart(chart_type, sales_df, result_by) # labels=gdf['transaction_id'].values)

            sales_df = sales_df.to_html()
            position_df = position_df.to_html()
            merged_df = merged_df.to_html()
            gdf = gdf.to_html()
        else:
            no_data = 'No data is available in this date range'

    ctxt = {
        'search_form': search_form,
        'report_form': report_form,
        'sales_df': sales_df,
        'position_df': position_df,
        'merged_df': merged_df,
        'gdf': gdf,
        'chart': chart,
        'no_data': no_data,
    }
    return render(request, 'sales/home.html', ctxt)

class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/main.html'
    # context_object_name = 'qs' would replace object_list in the view main.html

class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/detail.html'
