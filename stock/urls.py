from django.urls import path
from stock.views import add_stock,update_stock

app_name = 'stock'

urlpatterns = [
    path("add",add_stock, name="add_stock"),
    path("update/<id>", update_stock, name="update_stock")
]
