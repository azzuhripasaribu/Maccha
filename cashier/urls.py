from django.urls import path
from cashier.views import cashier

app_name = 'cashier'

urlpatterns = [
    path('', cashier, name='main'),
]