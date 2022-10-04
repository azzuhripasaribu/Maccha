from urllib import response
from django.test import TestCase, Client
from django.urls import reverse
from account.models import Account

# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register_page')
        self.login_url = reverse('login_page')
        self.profile_url = reverse('profile_page')
        self.logout_url = reverse('logout_page')
        self.homepage_url = reverse('homepage')
        self.user = {
            'email': 'test@email.com',
            'full_name': 'Full Name',
            'company_name': 'Company Name',
            'username': 'username',
            'password': 'password',
            'password_2': 'password'
        }
        self.user_diff_pass = {
            'email': 'test2@email.com',
            'full_name': 'Full Name',
            'company_name': 'Company Name',
            'username': 'username',
            'password': 'password',
            'password_2': 'password2'
        }

class RegisterTest(BaseTest):
    def test_can_access_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')

    def test_register_success(self):
        account = Account.objects.filter(email=self.user['email']).first()
        self.assertIsNone(account)
        response = self.client.post(self.register_url, self.user, format='text/html')
        account = Account.objects.filter(email=self.user['email']).first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(account.email, self.user['email'])

    def test_cant_register_different_password(self):
        response = self.client.post(self.register_url, self.user_diff_pass, format='text/html')
        account = Account.objects.filter(email=self.user_diff_pass['email']).first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(account)

class LoginTest(BaseTest):
    def test_can_access_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_success(self):
        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(self.login_url,self.user,format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_login_not_registered(self):
        response = self.client.post(self.login_url,self.user,format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context_data['form'])

class ProfileTest(BaseTest):
    def test_can_access_page(self):
        self.client.post(self.register_url, self.user, format='text/html')
        self.client.post(self.login_url,self.user,format='text/html')

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def update_profile_success(self):
        self.client.post(self.register_url, self.user, format='text/html')
        self.client.post(self.login_url,self.user,format='text/html')
        account = Account.objects.filter(email=self.user['email']).first()
        self.assertEqual('username', account.username)
        self.assertEqual('password', account.password)
        response = self.client.post(self.profile_url, {'username': 'new_username', 'password': 'new_password'}, format='text/html')
        self.assertEqual('new_username', account.username)
        self.assertEqual('new_password', account.password)

class LogoutTest(BaseTest):
    def test_logout_success(self):
        self.client.post(self.register_url, self.user, format='text/html')
        self.client.post(self.login_url,self.user,format='text/html')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)