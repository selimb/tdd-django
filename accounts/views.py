from django.urls import reverse
from django.contrib import messages, auth
from django.http import HttpRequest
from django.shortcuts import redirect
from django.core import mail

from .models import Token


def send_login_email(request: HttpRequest):
    email = request.POST["email"]
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse("login")) + f"?token={token.uid}"
    mail.send_mail(
        "Your login link for Superlists",
        f"Use this link to log in:\n\n{url}",
        "noreply@superlists",
        [email],
    )
    messages.success(
        request, "Check your email, we've sent you a link you can use to log in."
    )
    return redirect("/")


def login(request: HttpRequest):
    user = auth.authenticate(request.GET["token"])
    if user:
        auth.login(request, user)
    return redirect("/")
