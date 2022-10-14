import imp
from django.urls import path
from dashboard.views import dashboard, add_menu

urlpatterns = [
    path('',dashboard, name='dashboard'),
    path('add_menu',add_menu, name='add_menu')
]