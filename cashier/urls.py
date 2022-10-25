from django.urls import path
from cashier.views import cashier

urlpatterns = [
    path('checkout/',cashier, name='checkout')
]