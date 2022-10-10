import re
from unicodedata import name
from django.shortcuts import redirect, render
from requests import request
from menu.forms import MenuForm
from .models import menuModel
from django.contrib.auth.decorators import login_required


@login_required(login_url="../account/login")
def home(request):
    menu = menuModel.objects.all()
    context = {
        'menu':menu
    }
    return render(request, "menu.html",context)


@login_required(login_url="../account/login")
def add_menu(request) : 
    if request.method == "POST":
        form = MenuForm(request.POST or None)
        if form.is_valid():
            user = request.user
            name = request.POST.get('name')
            price = request.POST.get('price')
            description = request.POST.get('description')
            menu = menuModel(user=user,name = name, price=price, description = description)
            menu.save()
            return redirect('menu')
    form = MenuForm()
    context = {
        "form":form
    }
    return render(request,"add-menu.html",context)

@login_required(login_url="../account/login")
def edit_menu(request,menu_id) : 
    menu = menuModel.objects.get(id = menu_id)
    if request.user == menu.user:
        if request.method == "POST":
            form = MenuForm(request.POST, instance=menu)
            if form.is_valid():
                data = form.save(commit = False)
                data.save()
                return redirect('/menu')
        else:
            form = MenuForm(instance=menu)
            return render(request, 'edit-menu.html', {'form':form})
    else:
            return redirect('/menu')
            
@login_required(login_url="../account/login")
def delete_menu(request, menu_id):
    menu = menuModel.objects.get(id=menu_id)
    menu.delete()
    return redirect('/menu')
   