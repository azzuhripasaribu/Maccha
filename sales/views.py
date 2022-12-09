import json
from django.shortcuts import render
from django.http import JsonResponse
from cart.models import Cart, CartItem
from menu.models import menuModel
from django.contrib.auth.decorators import login_required

@login_required(login_url="login_page")
def sale_history(request):
    total_income = 0
    total_item = 0
    if request.user.is_authenticated:
        cart= Cart.objects.filter(user=request.user, completed=True)
        for i in cart:
            total_income += i.grand_total_price
            total_item += i.num_of_items

    context = {
        "cart":cart,
        "total_income" : total_income,
        "total_item": total_item
    }
    return render(request, "transaction_history.html", context)

@login_required(login_url="login_page")
def sale_details(request, cart_id):
    cart = None
    cartitems=[]
    if request.user.is_authenticated:
        cart = Cart.objects.get(user = request.user , id = cart_id)
        cartitems = cart.cartitems.all()

    context = {
        "cart":cart,
        "items":cartitems,
    }
    return render(request, "transaction_details.html", context)

@login_required(login_url="login_page")
def item_detail(request):
    menu = menuModel.objects.filter(user=request.user)
    carts = Cart.objects.filter(user=request.user)
    item_count = {}

    for transaction in carts:
        cart_items = CartItem.objects.filter(cart=transaction)
        for item in cart_items:
            if item.product.name not in item_count.keys():
                item_count[item.product.name] = 0
            
            item_count[item.product.name] += 1

    
        


    context = {
        'menu_items': item_count
    }
    return render(request,'item_details.html', context)
