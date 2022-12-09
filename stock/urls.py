from django.urls import path
from stock.views import add_stock,update_stock,home,delete_stock

app_name = 'stock'

urlpatterns = [
    path('',home, name='stock'),
    path("add",add_stock, name="add_stock"),
    path("update/<id>", update_stock, name="update_stock"),
    path('delete-stock/<int:stock_id>',delete_stock, name='delete-stock'),
]
