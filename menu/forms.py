from menu.models import menuModel
from django.db import models
from django.forms import ModelForm

class MenuForm(ModelForm):
    class Meta:
        model = menuModel
        fields = ["name","price","description"]
