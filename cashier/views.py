from django.shortcuts import render
from menu.models import menuModel

# Create your views here.
def cashier(request):
    MenuItems = menuModel.objects.filter()
    return render(request, 'cashier.html', {})