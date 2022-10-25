from cashier.models import Cashier
from django import forms

class CashierForm(forms.ModelForm):
    class Meta:
        model = Cashier
        fields = ["menu_id","itemQty"]

        widgets = {
            'itemQty': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"e.g. 50000",'id':'itemQty'}),
        }
        