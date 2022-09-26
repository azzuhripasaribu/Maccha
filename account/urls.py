from django.urls import path
from account.views import RegisterView , LoginView, homepage, logout_request

urlpatterns =[
    path('', homepage, name='homepage'),
    path('register', RegisterView.as_view(), name='register_page'),
    path('login', LoginView.as_view(), name='login_page'),
    path('logout', logout_request, name='logout_page'),
]