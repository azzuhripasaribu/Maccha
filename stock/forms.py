from stock.models import Stock
from menu.models import menuModel
from django import forms

class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs,):
        user = kwargs.pop('user')
        super(StockForm, self).__init__(*args,**kwargs)
        self.fields['menu'] = forms.ModelMultipleChoiceField(
            widget = forms.CheckboxSelectMultiple,
            queryset=menuModel.objects.filter(user=user)
        )
    class Meta:
        model = Stock
        fields = ["name","quantity","menu"]

    
    name = forms.TextInput()
    quantity = forms.IntegerField()
