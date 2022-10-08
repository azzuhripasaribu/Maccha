from django.urls import path
from menu.views import addMenu

urlpatterns = [
    path('', addMenu, name='addMenu')   
]
