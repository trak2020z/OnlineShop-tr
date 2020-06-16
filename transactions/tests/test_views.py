from django.test import TestCase, Client
from django.urls import reverse

from ..models import Order, Ordered
from ..views import new_order

from store.models import Product, Cart, CartLine

class TestTransactionsViews(TestCase):

    def setUp(self):
        self.client = Client()

        product1 = Product.objects.create(
            name='product1',
            category='category1',
            description='',
            price=10.00
        )
        product2 = Product.objects.create(
            name='product2',
            category='category2',
            description='',
            price=15.00
        )
        product3 = Product.objects.create(
            name='product3',
            category='category1',
            description='',
            price=2.35
        )
        session = self.client.session
        cart = {
            str(product1.id): 2,
            str(product2.id): 1,
            str(product3.id): 3,
        }
        session['cart'] = cart
        session.save()
    
    def test_views_new_order_POST(self):
        response = self.client.post(reverse('transactions:new_order'), {
            'name':             'test_name',
            'surname':          'test_surname',
            'email':            'email@example.com',
            'phone_number':     '123456789',
            'street_name':      'example 1',
            'zip_code':         '01-234',
            'city_name':        'City',
            'payment_type':     1,
            'shipping_type':    1
        })
        order = Order.objects.first()
        ordered = Ordered.objects.filter(order=order)
        
        self.assertEquals(order.name, 'test_name')
        self.assertEquals(len(ordered), 3)
