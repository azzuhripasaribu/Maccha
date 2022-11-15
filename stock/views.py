from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from stock.models import Stock
from stock.forms import StockForm

@login_required(login_url="../account/login")
def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        user = request.user
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')

        if form.is_valid():
            stock = Stock(user=user,name = name, quantity=quantity)
            stock.save()    
            return redirect('dashboard')
        return redirect('stock:add_stock')
    form = StockForm()
    context = {
        "form":form
    }
    return render(request,'add_stock.html', context)