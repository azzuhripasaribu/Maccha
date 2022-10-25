from django.shortcuts import render, redirect
from menu.models import menuModel
from cashier.models import Cashier
from cashier.forms import CashierForm
# Create your views here.
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


@login_required(login_url="../account/login")
def add_cashier(request) : 
    menu = menuModel.objects.filter(user = request.user)    
    if request.method == "POST":
        form = CashierForm(request.POST or None)
        user = request.user
        itemQty = request.POST.get('itemQty')
        menuId = request.POST.get('menu_id')
        menuObj = menuModel.objects.get(id = menuId)
        if form.is_valid():
            cashier = Cashier(user=user,menu_id = menuId, itemQty = itemQty, menu_object = menuObj)
            cashier.save()    
            return redirect('checkout')
        else:
            return redirect('checkout')
        # else:
        #     if int(price) <= 0:
        #         messages.error(request, f'Please Correct your Price, Price cannot be below 0 or 0')
        #     elif menuModel.objects.filter(name=name).exists():
        #         messages.error(request, "Menu name already exists")

            # return redirect('add-menu')
    form = CashierForm()
    context = {
        'menu':menu,
        "form":form,
    }
    return render(request,"cashiers.html",context)