from django.shortcuts import render
from django.views.generic import ListView, DetailView
import pandas as pd

from .models import Sale
from .forms import SalesSearchForm


# Create your views here.
def home_view(request):
    ## function views
    form = SalesSearchForm(request.POST or None)
    sales_df = None

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')

        qs = Sale.objects.filter(created_at__date__lte=date_to,  created_at__date__gte=date_from) # queryset
        if len(qs) > 0:
            print(" ##### ")
            sales_df = pd.DataFrame(qs.values())
            print(sales_df)
            sales_df = sales_df.to_html()
            print(" ##### ")
        else:
            print("No data")

    ctxt = {
        'form': form,
        'sales_df': sales_df
    }
    return render(request, 'sales/home.html', ctxt)

class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'
    # context_object_name = 'qs' would replace object_list in the view main.html

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'
