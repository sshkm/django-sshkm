from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def auth_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username is None:
        username = ''

    if password is None:
        password = ''

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/keymaster')
    else:
        return render(request, 'authentication/login.html')

@login_required
def auth_logout(request):
    logout(request)
    return redirect('/keymaster')
