from django.http import HttpRequest
from django.shortcuts import redirect


def send_login_email(request: HttpRequest):
    return redirect("/")


# Create your views here.
