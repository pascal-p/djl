from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Sale
from .forms import SalesSearchForm


# Create your views here.
def home_view(request):
    form = SalesSearchForm(request.POST or None)
    ## function views
    hw = "hello world from the view"
    ctxt = {
        'hello': hw,
        'form': form
    }
    return render(request, 'sales/home.html', ctxt)

class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'
    # context_object_name = 'qs' would replace object_list in the view main.html

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'
