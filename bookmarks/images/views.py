from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ImageCreateForm
from .models import Image
from common.decorators import ajax_required


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

    return render(request, 'images/image/create.html',
                  {'section': 'images', 'form': form})

@login_required
def image_list(request):
    imgs = Image.objects.all()
    paginator = Paginator(imgs, 5)
    page = request.GET.get('page')
    try:
        imgs = paginator.page(page)

    except PageNotAnInteger:
        imgs = paginator.page(1)

    except EmptyPage:
        if request.is_ajax():
            ## If the request is AJAX and page is out of range => empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        imgs = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': imgs})

    return render(request, 'images/image/list.html', {'section': 'images', 'images': imgs})

@ajax_required
@login_required
@require_POST
def image_like(request):
    img_id = request.POST.get('id')
    action = request.POST.get('action')
    if img_id and action:
        try:
            img = Image.objects.get(id=img_id)
            if action == 'like':
                img.users_like.add(request.user)
            else:
                img.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html',
                  {'section': 'images', 'image': image})
