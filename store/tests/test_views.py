from django.test import TestCase, Client
from django.urls import reverse

from store.models import Product
from store.views import ITEMS_ON_PAGE

import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        Product.objects.create(
            name='product1',
            category='category1',
            description='',
            price=10.00
        )
        Product.objects.create(
            name='product2',
            category='category2',
            description='',
            price=15.00
        )
        Product.objects.create(
            name='product3',
            category='category1',
            description='',
            price=2.35
        )
        Product.objects.create(
            name='product4',
            category='category1',
            description='',
            price=1.25
        )
        Product.objects.create(
            name='product5',
            category='category3',
            description='',
            price=0.25
        )
        Product.objects.create(
            name='product6',
            category='category3',
            description='',
            price=123.25
        )
        
    
    def test_store_index(self):
        response = self.client.get(reverse('store:index'))
        self.assertTemplateUsed(response, 'store/index.html')
    

    def test_store_list_no_parameters(self):
        response = self.client.get(reverse('store:list'))

        self.assertTemplateUsed(response, 'store/list.html')
        self.assertEquals(len(response.context['products']), ITEMS_ON_PAGE)
    

    # def test_store_list_one_parameter(self):
    #     response = self.client.get(reverse('store:list', kwargs={'page': 2}))

    #     self.assertTemplateUsed(response, 'store/list.html')
    #     self.assertEquals(len(response.context['products']), 1)
    

    # def test_store_list_two_parameters(self):
    #     response = self.client.get(reverse('store:list', kwargs={'page': 1, 'category': 'category1'}))

    #     self.assertTemplateUsed(response, 'store/list.html')
    #     self.assertEquals(len(response.context['products']), 3)
    

    def test_store_details(self):
        product_id = Product.objects.get(name='product2').id
        response = self.client.get(reverse('store:details', kwargs={'product_id': product_id}))

        self.assertTemplateUsed(response, 'store/details.html')
        self.assertEquals(response.context['product'].name, 'product2')
    
    def test_store_details_wrong_parameter(self):
        response = self.client.get(reverse('store:details', kwargs={'product_id': 136}))
        self.assertEquals(response.status_code, 304)
    

    def test_store_cart(self):
        # TODO: check for cart items

        response = self.client.get(reverse('store:cart'))
        self.assertTemplateUsed(response, 'store/shopping_cart.html')


    # # TU COS NIE DZIALA ZOSTAWIC NA RAZIE 
    # def test_add_to_cart(self):
    #     # TODO: adding product to session cart
    #     kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
    #     cart = {
    #         'item': Product.objects.first().id
    #     }
    #     response = self.client.get('store:add_to_cart', cart, **kwargs)
    #     self.assertEquals(response.status_code, 302)
    #     # TODO: check json data
        

    # # TU COS NIE DZIALA ZOSTAWIC NA RAZIE 
    # def test_remove_from_cart(self):
    #     # TODO: remove product from session cart
    #     kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
    #     cart = {
    #         'item': Product.objects.first().id
    #     }
    #     response = self.client.get('store:remove_from_cart', cart['item'])
    #     self.assertEquals(response.status_code, 302)
    #     # TODO: check json data
        