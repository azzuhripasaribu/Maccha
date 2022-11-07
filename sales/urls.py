from unicodedata import name
from django.urls import path
from sales.views import sale_history, item_detail
app_name = 'sales'

urlpatterns = [
    path("",sale_history, name="sale_history"),
    path("items",item_detail, name="item_detail")
]

# THIS