from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages


def index(request):
    return HttpResponse(
        """
        <h1>Hello, world. You're at the polls index.</h1>
        <ul>
            <li><a href="{}">Login</a></li>
            <li><a href="{}">Register</a></li>
        </ul>
        """.format(
            reverse("login"), reverse("register")
        )
    )


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "main/login.html")
    return render(request, "main/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, "main/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "main/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, "main/register.html")

        user = User.objects.create_user(
            username=username, email=email, password=password1
        )
        user.save()

        login(request, user)
        return redirect("dashboard")

    return render(request, "main/register.html")
