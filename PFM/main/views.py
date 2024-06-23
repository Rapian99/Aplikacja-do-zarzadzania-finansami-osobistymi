from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse


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
    return HttpResponse("This is the login page.")


def register_view(request):
    return HttpResponse("This is the registration page.")
