from django.test import TestCase, Client
from django.urls import reverse, resolve
from sales.views import sale_history

class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register_page')
        self.login_url = reverse('login_page')
        self.sales_url = reverse('sales:sale_history')

        self.user = {
            'email': 'test@email.com',
            'full_name': 'Full Name',
            'company_name': 'Company Name',
            'username': 'username',
            'password': 'password',
            'password_2': 'password'
        }
        self.client.post(self.register_url, self.user, format='text/html')

class TestUrls(BaseTest):
    def test_sales_history_url_is_resolved(self):
        self.assertEqual(resolve(self.sales_url).func, sale_history)

class TestViews(BaseTest):
    def test_sales_history_unauthenticated_access(self):
        response = self.client.get(self.sales_url)
        self.assertEqual(response.status_code,302)

    def test_sales_history_authenticated_access(self):
        self.client.post(self.login_url,self.user,format='text/html')
        response = self.client.get(self.sales_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transaction_history.html')

        
        

