from django.test import TestCase, Client
from django.urls import reverse, resolve
from stock.views import add_stock, update_stock
from stock.models import Stock
from account.models import Account
from menu.models import menuModel

class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register_page')
        self.login_url = reverse('login_page')
        self.logout_url = reverse('logout_page')
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
        
        self.user2 = {
            'email': 'test2@email.com',
            'full_name': 'Full Name new',
            'company_name': 'Company 2 Name',
            'username': 'username2',
            'password': 'password2',
            'password_2': 'password2'
        }

        self.menu1 = {
            'id' : 1,
            'user' : 'test@email.com',
            'name' : 'ayam',
            'price' : 50000,
            'description' : 'hewan berbulu'
        }

        self.menu2 = {
            'id' : 2,
            'user' : 'test@email.com',
            'name' : 'ayam goreng',
            'price' : 50000,
            'description' : 'hewan berbulu, tapi di goreng'
        }

        self.stock = {
            'id':1,
            'name': 'ayam',
            'quantity': 20,
            'menu': 1
        }

        self.stock_update = {
            'id': 1,
            'name': 'ayam',
            'quantity': 20,
            'menu': [1,2]
        }
        self.update_stock_url = reverse('stock:update_stock',kwargs={'id':self.stock_update['id']})

        self.stock_invalid = {
            'id': 1,
            'name': 'ayam',
            'quantity': 'dua puluh',
            'menu': 1
        }

        # Registers test client accounts
        self.client.post(self.register_url, self.user, format='text/html')
        self.client.post(self.register_url, self.user2, format='text/html')


class TestUrls(BaseTest):
    def test_add_stock_url_is_resolved(self):
        self.assertEqual(resolve(self.add_stock_url).func, add_stock)
    
    def test_update_stock_url_is_resolved(self):
        self.assertEqual(resolve(self.update_stock_url).func, update_stock)
    
class TestViews(BaseTest):
    def test_add_stock_unauthenticated_access(self):
        response = self.client.get(self.add_stock_url)
        self.assertEqual(response.status_code,302)
    
    def test_add_stock_authenticated_access(self):
        self.client.post(self.login_url,self.user,format='text/html')
        response = self.client.get(self.add_stock_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_stock.html')
        
    def test_add_stock_post(self):
        # Logs in test client
        self.client.post(self.login_url,self.user,format='text/html')

        # Add menu to database
        self.client.post(self.addmenu_url,self.menu1,format ='text/html')

        # Add stock to database
        response = self.client.post(self.add_stock_url,self.stock,format ='text/html')

        self.assertEqual(response.status_code,302)

        dummy_stock = Stock.objects.filter(name = self.stock['name']).first()
        dummy_user = Account.objects.get(email=self.user['email'])
        dummy_menu = menuModel.objects.get(id=self.menu1['id'])

        self.assertEqual(dummy_stock.user, dummy_user)
        self.assertEqual(dummy_stock.quantity,self.stock['quantity'])
        self.assertEqual(dummy_stock.menu.get(id=dummy_menu.id),dummy_menu)

    def test_add_stock_post_invalid(self):
        # Logs in test client
        self.client.post(self.login_url,self.user,format='text/html')

        # Add menu to database
        self.client.post(self.addmenu_url,self.menu1,format ='text/html')

        # Add stock to database
        response = self.client.post(self.add_stock_url,self.stock_invalid,format ='text/html')

        self.assertRedirects(response,self.add_stock_url,302,200,'',True)

    def test_update_stock_unauthenticated_access(self):
        response = self.client.get(self.update_stock_url)
        redirect_url = self.login_url + '?next=' + self.update_stock_url
        self.assertRedirects(response,redirect_url,302,200)
    
    def test_update_stock_unauthorized_access(self):
        # logs in test client
        self.client.post(self.login_url,self.user,format='text/html')

        # Add menu to database
        self.client.post(self.addmenu_url,self.menu1,format ='text/html')

        # Add stock to database
        self.client.post(self.add_stock_url,self.stock,format ='text/html')

        # logs out client
        self.client.get(self.logout_url)

        # logs in test client with different account
        self.client.post(self.login_url,self.user2,format='text/html')

        response = self.client.get(self.update_stock_url)
        self.assertRedirects(response,reverse('dashboard'),302,200,'',True)


    def test_update_stock_authenticated_access(self):
        # logs in test client
        self.client.post(self.login_url,self.user,format='text/html')

        # Add menu to database
        self.client.post(self.addmenu_url,self.menu1,format ='text/html')

        # Add stock to database
        self.client.post(self.add_stock_url,self.stock,format ='text/html')

        response = self.client.get(self.update_stock_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_stock.html')

    def test_update_stock_post(self):
        # Logs in test client
        self.client.post(self.login_url,self.user,format='text/html')

        # Add menu to database
        self.client.post(self.addmenu_url,self.menu1,format ='text/html')
        self.client.post(self.addmenu_url,self.menu2,format ='text/html')

        # Add stock to database
        self.client.post(self.add_stock_url,self.stock,format ='text/html')

        # Update stock in database
        response = self.client.post(self.update_stock_url,self.stock_update,format ='text/html')

        self.assertEqual(response.status_code,302)

        dummy_stock = Stock.objects.filter(name = self.stock['name']).first()
        dummy_user = Account.objects.get(email=self.user['email'])
        dummy_menu = menuModel.objects.filter(id__in=self.stock_update['menu'])
        

        self.assertEqual(dummy_stock.user, dummy_user)
        self.assertEqual(dummy_stock.quantity,self.stock['quantity'])
        self.assertQuerysetEqual(list(dummy_stock.menu.all()), dummy_menu)

    def test_update_stock_post_invalid(self):
        # Logs in test client
        self.client.post(self.login_url,self.user,format='text/html')

        # Add menu to database
        self.client.post(self.addmenu_url,self.menu1,format ='text/html')
    
        # Add stock to database
        self.client.post(self.add_stock_url,self.stock,format ='text/html')

        # Update stock in database
        response = self.client.post(self.update_stock_url,self.stock_invalid,format ='text/html')

        self.assertRedirects(response,self.update_stock_url,302,200,'',True)


    
