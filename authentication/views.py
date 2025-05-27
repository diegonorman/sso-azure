from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse

# Página de login personalizada

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return render(request, 'authentication/login.html', {'error': 'Usuário ou senha inválidos.'})
    return render(request, 'authentication/login.html')

# Logout

def custom_logout(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

# Dashboard pós-login
@login_required
def dashboard(request):
    return render(request, 'authentication/dashboard.html')
