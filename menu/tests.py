from django.test import TestCase, Client
from django.urls import reverse

class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register_page')
        self.login_url = reverse('login_page')
        self.menu_url = reverse('menu')
        self.user = {
            'email': 'test@email.com',
            'full_name': 'Full Name',
            'company_name': 'Company Name',
            'username': 'username',
            'password': 'password',
            'password_2': 'password'
        }
        self.client.post(self.register_url, self.user, format='text/html')

class MenuTest(BaseTest):
    def test_unauthenticated_access(self):
        response = self.client.get(self.menu_url)
        self.assertEqual(response.status_code,302)

    def test_authenticaed_access(self):
        self.client.post(self.login_url,self.user,format='text/html')
        response = self.client.get(self.menu_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"menu.html")
           