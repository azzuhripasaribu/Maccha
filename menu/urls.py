from django.urls import path
from menu.views import home,add_menu, edit_menu,delete_menu



urlpatterns = [
    path('',home, name='menu'),
     path('edit-menu/<int:menu_id>',edit_menu, name='edit-menu'),
    path('add-menu',add_menu, name='add-menu'),
    path('delete-menu/<int:menu_id>',delete_menu, name='delete-menu'),
]
