from django.db import models


class Item(models.Model):
    text: str = models.TextField(default="")
