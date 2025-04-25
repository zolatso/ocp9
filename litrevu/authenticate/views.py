from django.contrib.auth import logout, login
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from . import forms


def logout_user(request):
    logout(request)
    return redirect('login')

def sign_up(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authenticate/sign_up.html', context={'form': form})
