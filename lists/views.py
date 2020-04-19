from django.http import HttpRequest
from django.shortcuts import redirect, render

from lists.models import Item


def home_page(request: HttpRequest):
    return render(request, "home.html")


def new_list(request: HttpRequest):
    Item.objects.create(text=request.POST["item_text"])
    return redirect("/lists/the-only-list-in-the-world/")


def view_list(request: HttpRequest):
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})
