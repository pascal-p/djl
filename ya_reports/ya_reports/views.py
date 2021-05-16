from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    err_msg = None
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned.get('username')
            passwd = form.cleaned.get('password')
            user = authenticate(username=username, password=passwd)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('sales:home')
        else:
            err_msg = "OOopsss... Something went wrong"
    ctxt = {
        'form': form,
        'error_message': err_msg,
    }
    return render(request, 'auth/login.html', ctxt)

def logout_view(request):
    logout(request)
    return redirect('login')
