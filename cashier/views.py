from django.shortcuts import render, redirect
from menu.models import menuModel
from cashier.models import Cashier
import re
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required(login_url="../account/login")
def cashier(request):
    cashier = Cashier.objects.filter(user = request.user)
    context = {
        'cashier':cashier,
    }
    return render(request, "checkout.html",context)