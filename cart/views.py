# Create your views here.
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from cart.models import Cart, CartItem
from menu.models import menuModel
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="../account/login")
def cart_index(request):
    products = menuModel.objects.filter(user=request.user)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    context = {
        "products":products,
        "cart":cart,
    }
    return render(request, "cashier_index.html", context)

@login_required(login_url="../account/login")
def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = menuModel.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()

        num_of_item = cart.num_of_items
        print(cartitem)
    return JsonResponse(num_of_item, safe=False)