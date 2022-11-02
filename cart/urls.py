from unicodedata import name
from django.urls import path
from .views import cart_index, add_to_cart, cart_list,payment, payment_success
urlpatterns = [
    path("",cart_index, name="index"),
    path("add_to_cart",add_to_cart, name="add_to_cart"),
    path("list",cart_list, name="cart"),
    path("payment",payment, name="payment"),
    path("payment_success",payment_success, name="payment_success"),
]

# THIS