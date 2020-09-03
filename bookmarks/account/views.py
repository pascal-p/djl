from django.shortcuts import render
from django.contrib.auth.decorators import login_required

## Create your views here.
from .forms import LoginForm, UserRegistrationForm

## FBV
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False) ## Create a new user object but avoid saving it yet
            new_user.set_password(                  ## Set the chosen password - handle hashing
                user_form.cleaned_data['password']
            )
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

## TODO: if possible convert to CBV
