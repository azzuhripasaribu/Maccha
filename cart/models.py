from django.db import models

# Create your models here.
from django.db import models
import uuid
from account.models import Account
from menu.models import menuModel
# Create your models here.
class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def grand_total_price(self):
        cartitems = self.cartitems.all()
        total = sum([item.price for item in cartitems])
        return total

    @property
    def num_of_items(self):
        cartitems = self.cartitems.all()
        quantity = sum([item.quantity for item in cartitems])
        return quantity


class CartItem(models.Model):
    product = models.ForeignKey(menuModel, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name

    @property
    def price(self):
        new_price = self.product.price * self.quantity
        return new_price