from django.urls import path
from stock.views import add_stock

app_name = 'stock'

urlpatterns = [
    path("add",add_stock, name="add_stock"),
]
