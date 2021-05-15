from django.shortcuts import render

# Create your views here.
def home_view(request):
    ## function views
    hw = "hello world from the view"
    return render(request, 'sales/main.html', {'h': hw})
