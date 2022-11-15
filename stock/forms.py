from stock.models import Stock
from django import forms

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["name","quantity"]

        widgets = {
            'name': forms.TextInput(),
            'price': forms.IntegerField(),
        }
