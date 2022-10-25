from django.test import TestCase, Client
from django.urls import reverse, resolve
from cashier.views import cashier
from menu.models import menuModel
import datetime

class TestCashier(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.cashier_url = reverse('cashier:main')

    def test_cashier_url_is_resolved(self):
        self.assertEqual(resolve(self.cashier_url).func, cashier)

    def test_cashier_view_get(self):
        response = self.client.get(self.cashier_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cashier.html')
    


