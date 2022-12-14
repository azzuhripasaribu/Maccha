from unicodedata import name
from django.urls import path
from .views import cart_index, add_to_cart, cart_list,payment
app_name = 'cart'

urlpatterns = [
    path("",cart_index, name="index"),
    path("add_to_cart",add_to_cart, name="add_to_cart"),
    path("list",cart_list, name="cart"),
    path("payment",payment, name="payment"),
]

# THIS