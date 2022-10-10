from django.urls import path
from menu.views import home,add_menu



urlpatterns = [
    path('',home, name='menu'),
    path('add-menu',add_menu, name='add-menu'),
]