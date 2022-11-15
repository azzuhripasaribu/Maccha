from django.test import TestCase, Client
from django.urls import reverse, resolve
from stock.views import add_stock
from stock.models import Stock
from account.models import Account

class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register_page')
        self.login_url = reverse('login_page')
        self.addmenu_url = reverse('add-menu')
        self.add_stock_url = reverse('stock:add_stock')

        self.user = {
            'email': 'test@email.com',
            'full_name': 'Full Name',
            'company_name': 'Company Name',
            'username': 'username',
            'password': 'password',
            'password_2': 'password'
        }
        

        self.menu = {
            'id' : 1,
            'user' : 'test@email.com',
            'name' : 'ayam',
            'price' : 50000,
            'description' : 'hewan berbulu'
        }

        self.stock = {
            'name': 'ayam',
            'quantity': 20,
            'menu': 'ayam',
        }

        # Registers test client
        self.client.post(self.register_url, self.user, format='text/html')


class TestUrls(BaseTest):
    def test_add_stock_url_is_resolved(self):
        self.assertEqual(resolve(self.add_stock_url).func, add_stock)
    
class TestViews(BaseTest):
    def test_add_stock_unauthenticated_access(self):
        response = self.client.get(self.add_stock_url)
        self.assertEqual(response.status_code,302)
    
    def test_add_stock_authenticated_access(self):
        self.client.post(self.login_url,self.user,format='text/html')
        response = self.client.get(self.add_stock_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_stock.html')
        
    def test_add_menu_post(self):
        # Logs in test client
        self.client.post(self.login_url,self.user,format='text/html')

        # Add menu to database
        self.client.post(self.addmenu_url,self.menu,format ='text/html')

        # Add stock to database
        response = self.client.post(self.add_stock_url,self.stock,format ='text/html')

        self.assertEqual(response.status_code,302)

        dummy_stock = Stock.objects.filter(name = self.stock['name']).first()
        dummy_user = Account.objects.get(email=self.user['email'])
        self.assertEqual(dummy_stock.user, dummy_user)
        self.assertEqual(dummy_stock.quantity,self.stock['quantity'])
    
