from unicodedata import name
from django.urls import path
from .views import cart_index, cart_list, add_to_cart, delete_from_cart, payment, payment_success
urlpatterns = [
    path("",cart_index, name="index"),
    path("add_to_cart",add_to_cart, name="add_to_cart"),
]