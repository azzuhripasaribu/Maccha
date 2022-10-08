from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def addMenu(request):
    return render(request,"AddMenu.html", {})