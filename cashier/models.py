from email.policy import default
from django.db import models
from account.models import Account
from menu.models import menuModel

# Create your models here.
class Cashier(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    menu_id = models.IntegerField()
    menu_object = models.ForeignKey(menuModel, on_delete=models.CASCADE)
    itemQty = models.IntegerField()
    cashierCreate = models.DateTimeField(auto_now_add=True)