# Create your views here.
import json
from django.shortcuts import render
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


@login_required(login_url="../account/login")
def cart_list(request):
    cart=None
    cartitems=[]
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitems = cart.cartitems.all()

    context = {
        "cart":cart,
        "items":cartitems,
    }
    return render(request, "cashier_list.html", context)


@login_required(login_url="../account/login")
def payment(request):  
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user)
        grand_total = cart[0].grand_total_price
        paid_amount = request.POST.get('amount')
        paid_amount_int = int(paid_amount)

        if paid_amount_int >= grand_total:
            cart.update(completed=True)  # 🖘 save the update in the database
            return render(request, 'payment_success.html')
              
    cart=None
    grand_total = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        grand_total = cart.grand_total_price
    context = {
        "cart":cart,
        "grand_total":grand_total,
    }
    return render(request, "payment.html", context)
