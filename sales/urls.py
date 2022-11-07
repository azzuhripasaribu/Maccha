from unicodedata import name
from django.urls import path
from sales.views import sale_history, sale_details
app_name = 'sales'

urlpatterns = [
    path("",sale_history, name="sale_history"),
    path('sale_details/<str:cart_id>',sale_details, name='sale_details'),
]

# THIS