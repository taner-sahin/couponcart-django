from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "login.html")

from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect("home")