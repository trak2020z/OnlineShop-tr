from django.test import SimpleTestCase
from django.urls import reverse, resolve

from transactions.views import orders_list, order, payment

class TestUrls(SimpleTestCase):

    def test_order_list_url(self):
        url = reverse('transactions:list')
        self.assertEqual(resolve(url).func, orders_list)
    
    def test_order_url(self):
        url = reverse('transactions:order', kwargs={'order_id': 1})
        self.assertEqual(resolve(url).func, order)
    
    def test_payment_url(self):
        url = reverse('transactions:payment', kwargs={'order_id': 1})
        self.assertEqual(resolve(url).func, payment)