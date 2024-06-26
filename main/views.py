from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile


def index(request):
    return render(request,"main/index.html")




def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if (
                not user.is_staff
                and not user.is_superuser
                and not hasattr(user, "userprofile")
            ):
                UserProfile.objects.create(user=user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "main/login.html")
    return render(request, "main/login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

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
        if (
            not user.is_staff
            and not user.is_superuser
            and not hasattr(user, "userprofile")
        ):
            UserProfile.objects.create(user=user)
        return redirect("dashboard")

    return render(request, "main/register.html")


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            if hasattr(request.user, "userprofile"):
                request.user.userprofile.must_change_password = False
                request.user.userprofile.save()
            return redirect("dashboard")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "main/change_password.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")
