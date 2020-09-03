from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ImageCreateForm

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')
            return redirect(new_item.get_absolute_url())
        else:
            None
    else:
        form = ImageCreateForm(data=request.GET)  ## build form with data provided by the bookmarklet via GET
        
    return render(request, 'images/iamge/create.html',
                  {'section': 'images', 'form': form})
