from django.shortcuts import redirect, render

from .models import menuModel
from django.contrib.auth.decorators import login_required

@login_required(login_url="../account/login")
def home(request):
    menu = menuModel.objects.all()
    context = {
        'menu':menu
    }
    return render(request, "menu.html",context)
