import re
from unicodedata import name
from django.shortcuts import redirect, render
from requests import request
from menu.forms import MenuForm
from .models import menuModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url="login_page")
def home(request):
    menu = menuModel.objects.all()
    context = {
        'menu':menu
    }
    return render(request, "menu.html",context)


@login_required(login_url="login_page")
def add_menu(request) : 
    if request.method == "POST":
        user = request.user
        form = MenuForm(request.POST or None, user=user)
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        if form.is_valid():
            menu = menuModel(user=user,name = name, price=price, description = description)
            menu.save()    
            return redirect('menu')
        else:
            print(form.errors.as_data())
            # Checks if price is integer
            try:
                int(price)
            except ValueError:
                messages.error(request,f'Price must be integers')
                return redirect('add-menu')

            if int(price) <= 0:
                messages.error(request, f'Please Correct your Price, Price cannot be below 0 or 0')
            elif menuModel.objects.filter(name=name).exists():
                messages.error(request, "Menu name already exists")

            return redirect('add-menu')
    form = MenuForm(user=request.user)
    context = {
        "form":form
    }
    return render(request,"add-menu.html",context)

@login_required(login_url="login_page")
def edit_menu(request,menu_id) : 
    menu = menuModel.objects.get(id = menu_id)
    if request.user == menu.user:
        if request.method == "POST":
            form = MenuForm(request.POST, instance=menu)
            price = request.POST.get('price')
            if form.is_valid():
                data = form.save(commit = False)
                data.save()
                return redirect('/menu')
            else:
                # Checks if price is integer
                try:
                    int(price)
                except ValueError:
                    messages.error(request,f'Price must be integers')
                    return redirect('add-menu')

                if int(price) <= 0:
                    messages.error(request, f'Please Correct your Price, Price cannot be below 0 or 0')
                    return redirect('../edit-menu/'+str(menu_id))
                else:
                    messages.error(request, f'No Duplicate Menu Name Allowed!')
                    return redirect('../edit-menu/'+str(menu_id))
        else:
            form = MenuForm(instance=menu)
            return render(request, 'edit-menu.html', {'form':form})
    else:
            return redirect('/menu')
            
@login_required(login_url="login_page")
def delete_menu(request, menu_id):
    menu = menuModel.objects.get(id=menu_id)
    if menu.user == request.user:
        menu.delete()
    return redirect('/menu')
   
def cashier(request):
    menu = menuModel.objects.all()
    context = {
        'menu':menu
    }
    return render(request,'cashier.html',context)
