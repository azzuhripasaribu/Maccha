from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def dashboard(request):
    return render(request,'dashboard.html')

def add_menu(request):
    return render(request,'index.html')