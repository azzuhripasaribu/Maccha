from django.urls import path
from cashier.views import cashier, add_cashier

urlpatterns = [
    path('',add_cashier, name='cashiers'),
    path('checkout/',cashier, name='checkout')
]