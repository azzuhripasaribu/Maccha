from unicodedata import name
from django.urls import path
from .views import cart_index, add_to_cart
urlpatterns = [
    path("",cart_index, name="index"),
    path("add_to_cart",add_to_cart, name="add_to_cart"),
]