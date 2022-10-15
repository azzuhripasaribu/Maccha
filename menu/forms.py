from logging import PlaceHolder
from menu.models import menuModel
from django.db import models
from django import forms

class MenuForm(forms.ModelForm):
    class Meta:
        model = menuModel
        fields = ["name","price","description"]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"e.g. Ice Macchiato"}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"e.g. 50000"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':"Write Your Description Here"}),
        }
