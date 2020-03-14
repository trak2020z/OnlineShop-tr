from django.test import SimpleTestCase

from django.urls import reverse, resolve

from store.views import index, product_list, product_details, cart, add_to_cart, remove_from_cart


class TestUrls(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse('store:index')
        self.assertEqual(resolve(url).func, index)


    def test_list_urls_resolves(self):
        url_no_params = reverse('store:list', kwargs={})
        url_params_1 = reverse('store:list', kwargs={'page':1})
        url_params_2 = reverse('store:list', kwargs={'page':1, 'category':'sport'})

        self.assertEqual(resolve(url_no_params).func, product_list)
        self.assertEqual(resolve(url_params_1).func, product_list)
        self.assertEqual(resolve(url_params_2).func, product_list)


    def test_details_url_resolves(self):
        url = reverse('store:details', kwargs={'product_id':4})
        self.assertEqual(resolve(url).func, product_details)


    def test_cart_url_resolves(self):
        url = reverse('store:cart')
        self.assertEqual(resolve(url).func, cart)
    
    def test_add_to_cart_url_resolves(self):
        url = reverse('store:add_to_cart', {"product_id: 1"})
        self.assertEqual(resolve(url).func, add_to_cart)
    
    def test_remove_from_cart_url_resolves(self):
        url = reverse('store:remove_from_cart', {"product_id: 1"})
        self.assertEqual(resolve(url).func, remove_from_cart)