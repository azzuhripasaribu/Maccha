from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from stock.models import Stock
from menu.models import menuModel
from stock.forms import StockForm

@login_required(login_url="login_page")
def home(request):
    stock = Stock.objects.all()
    menu = {}
    for stockEntry in stock:
        menuStock = stockEntry.menu.all()
        menu[stockEntry.name] = ""
        for menuEntry in menuStock:
            menu[stockEntry.name] = menu[stockEntry.name] +f'{menuEntry}, '
        menu[stockEntry.name] = menu[stockEntry.name][0:-2]
        

    print(menu)
    context = {
        'stock':stock,
        'menu':menu
    }
    return render(request, "stock.html",context)

@login_required(login_url="login_page")
def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None,user = request.user)
        user = request.user
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        menu = request.POST.getlist('menu')

        if form.is_valid():
            stock = Stock(user=user,name = name, quantity=quantity)
            stock.save()
            for menuId in menu:
                menuObject = menuModel.objects.get(id=menuId)
                stock.menu.add(menuObject)
            return redirect('stock:stock')
        return redirect('stock:add_stock')
    form = StockForm(user=request.user)
    context = {
        "form":form
    }
    return render(request,'add_stock.html', context)

@login_required(login_url="login_page")
def update_stock(request, id):
    stock = Stock.objects.get(id=id)

    # handle user trying to access others stock
    if request.user != stock.user:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StockForm(request.POST,user = request.user, instance=stock)
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        menu = request.POST.getlist('menu')

        if form.is_valid():
            stock.name = name
            stock.quantity = quantity
            stock.menu.clear()
            stock.save()
            for menuId in menu:
                menuObject = menuModel.objects.get(id=menuId)
                stock.menu.add(menuObject)
            return redirect('stock:stock')
            
        return redirect('stock:update_stock',id = id)

    form = StockForm(user = request.user, instance=stock)
    context = {
        "form" : form
    }
    return render(request, 'update_stock.html', context)

@login_required(login_url="login_page")
def delete_stock(request, stock_id):
    stock = Stock.objects.get(id=stock_id)
    if stock.user == request.user:
        stock.delete()
        
    return redirect('/stock')