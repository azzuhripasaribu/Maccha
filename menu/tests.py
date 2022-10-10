from tkinter import Menu
from urllib import response
from django.test import TestCase, Client
from django.urls import reverse
from account.models import Account
from menu.models import menuModel


class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register_page')
        self.login_url = reverse('login_page')
        self.menu_url = reverse('menu')
        self.addmenu_url = reverse('add-menu')
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
        self.editmenu = {
            'name' : 'roti',
            'price' : 3000,
            'description' : 'ayam bakar'
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

    def test_add_menu_get(self):
        self.client.post(self.login_url,self.user,format='text/html')
        response = self.client.get(self.addmenu_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"add-menu.html")
    
    def test_unauthenticated_access_add_menu(self):
        response = self.client.get(self.addmenu_url)
        self.assertEqual(response.status_code,302)
    
    def test_add_menu_post(self):
        self.client.post(self.login_url,self.user,format='text/html')
        response = self.client.post(self.addmenu_url,self.menu,format ='text/html')
        dummy_menu = menuModel.objects.filter(name = 'ayam').first()
        self.assertEqual(dummy_menu.price,self.menu["price"])
        self.assertEqual(response.status_code,302)       
    
    def test_edit_menu_post(self):
        self.client.post(self.login_url,self.user,format='text/html')
        response = self.client.post(self.addmenu_url,self.menu,format ='text/html')
        dummy_menu = menuModel.objects.filter(name = 'ayam').first()
        self.assertEqual(dummy_menu.price,self.menu["price"])
        id = dummy_menu.id
        response = self.client.post(reverse("edit-menu", kwargs={"menu_id": id}),self.editmenu,format='text/html')
        dummy_menu = menuModel.objects.filter(name = 'roti').first()
        self.assertEqual(response.status_code,302)
        self.assertEqual(dummy_menu.name,self.editmenu["name"])
        self.assertEqual(dummy_menu.price,self.editmenu["price"])

    def test_edit_menu_get(self):
        self.client.post(self.login_url,self.user,format='text/html')
        response = self.client.post(self.addmenu_url,self.menu,format ='text/html')
        dummy_menu = menuModel.objects.filter(name = 'ayam').first()
        self.assertEqual(dummy_menu.price,self.menu["price"])
        id = dummy_menu.id
        response = self.client.get(reverse("edit-menu", kwargs={"menu_id": id}))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'edit-menu.html')

    def test_delete_menu(self):
        self.client.post(self.login_url,self.user,format='text/html')
        response = self.client.post(self.addmenu_url,self.menu,format ='text/html')
        dummy_menu = menuModel.objects.filter(name = 'ayam').first()
        self.assertEqual(dummy_menu.price,self.menu["price"])
        id = dummy_menu.id
        response = self.client.post(reverse("delete-menu", kwargs={"menu_id": id}),format='text/html')
        dummy_menu = menuModel.objects.filter(name = 'ayam').first()
        self.assertIsNone(dummy_menu)
        self.assertEqual(response.status_code,302)