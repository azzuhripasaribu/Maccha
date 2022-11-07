from django.test import TestCase, Client
from django.urls import reverse, resolve
from sales.views import sale_history
from cart.models import Cart,CartItem
from sales.views import sale_history, item_detail

class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register_page')
        self.login_url = reverse('login_page')
        self.sales_url = reverse('sales:sale_history')
        self.addmenu_url = reverse('add-menu')
        self.item_detail_url = reverse('sales:item_detail')

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
        self.client.post(self.register_url, self.user, format='text/html')

        self.sale_details = {
            'id' : "test",
        }
        # self.sales_details_url = reverse('sales:sale_details/' + str(self.sale_details['id']))
        


# class BaseDetails(BaseTest):
#     def detailSetUp(self):
#         self.client.post(self.addmenu_url,self.menu,format ='text/html')
#         cart = Cart.objects.create(id = "test", user = self.client, completed = True)
#         cart.save()
#         cartitem = CartItem.objects.create(product = self.menu, cart = cart, quantity = 1)
#         cartitem.save()




class TestUrls(BaseTest):
    def test_sales_history_url_is_resolved(self):
        self.assertEqual(resolve(self.sales_url).func, sale_history)
    
    def test_sales_item_details_url_is_resolved(self):
        self.assertEqual(resolve(self.item_detail_url).func, item_detail)
    

class TestViews(BaseTest):
    def test_sales_history_unauthenticated_access(self):
        response = self.client.get(self.sales_url)
        self.assertEqual(response.status_code,302)
    
    def test_sales_item_detail_unauthenticated_access(self):
        response = self.client.get(self.item_detail_url)
        self.assertEqual(response.status_code,302)

    def test_sales_history_authenticated_access(self):
        self.client.post(self.login_url,self.user,format='text/html')
        response = self.client.get(self.sales_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transaction_history.html')
    
    def test_sales_item_detail_authenticated_access(self):
        self.client.post(self.login_url,self.user,format='text/html')
        response = self.client.get(self.item_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'item_details.html')


    # def test_sales_details_unauthenticated_access(self):
    #     response = self.client.get(self.sales_details_url)
    #     self.assertEqual(response.status_code,302)

    # def test_sales_details_authenticated_access(self):


    #     self.client.post(self.login_url,self.user,format='text/html')
    #     response = self.client.get(self.sales_details_url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'transaction_details.html')

        
        

