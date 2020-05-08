from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.utils.html import escape

from lists.forms import ItemForm, ExistingListItemForm
from lists.models import Item, List


def home_page(request: HttpRequest):
    return render(request, "home.html", {"form": ItemForm()})


def new_list(request: HttpRequest):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, "home.html", {"form": form})


def view_list(request: HttpRequest, list_id: str):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, "list.html", {"list": list_, "form": form})
