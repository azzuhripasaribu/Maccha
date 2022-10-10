from django.db import models
from account.models import Account
from django.conf import settings

# Create your models here.
class menuModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    description = models.TextField()
    
    def __str__(self):
        return self.name