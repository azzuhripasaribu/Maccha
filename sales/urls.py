from unicodedata import name
from django.urls import path
from sales.views import sale_history
app_name = 'sales'

urlpatterns = [
    path("",sale_history, name="sale_history"),
]

# THIS