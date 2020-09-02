from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required

## Create your views here.
# from .forms import LoginForm

## FBV
# def user_login(request):
#     template = 'account/login.html'
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 # ...
#             else:
#                 return HttpResponse('Login invalid')
#         # ...
#     else:
#         ## Assume get - render empty forms
#         form = LoginForm()
#     return render(request, template, {'form': form})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

## TODO: if possible convert to CBV
