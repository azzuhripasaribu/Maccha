from logging import PlaceHolder
from menu.models import menuModel
from django.db import models
from django import forms
from django.core.exceptions import ValidationError

import gettext
_ = gettext.gettext

class MenuForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MenuForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = menuModel
        fields = ["name","price","description"]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"e.g. Ice Macchiato"}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"e.g. 50000"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':"Write Your Description Here"}),
        }
            
    def clean_name(self):
        data = self.cleaned_data["name"]
        # Checks if menu already exist
        menu = menuModel.objects.filter(name=data,user=self.user)
        if menu.exists():
            if not menu[0] == self.instance:
                print("THis")
                raise ValidationError(
                    _('Invalid value: %(value)s'),
                    code='MenuAlreadyExist',
                    params={'value': 'name'},
                )
        return data

    def clean_price(self):
        data = self.cleaned_data["price"]

        # Checks if the price is integer
        if not isInteger(data):
            raise ValidationError(
                _('Invalid value: %(value)s'),
                code='PriceNotInteger',
                params={'value': 'price'},
            )
        
        # Checks if price is greater than or equal to 0
        if data < 0:
            raise ValidationError(
                _('Invalid value: %(value)s'),
                code='PriceLessThanZero',
                params={'value': 'price'},
            )

        return data

    
    
def isInteger(data):
    try:
        num = float(data)
    except ValueError:
        return False
    return num.is_integer()