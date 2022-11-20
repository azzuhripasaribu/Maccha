from django.db import models
from django.conf import settings
from menu.models import menuModel;

class Stock(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    menu = models.ManyToManyField(menuModel)


