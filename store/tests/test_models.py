from django.test import TestCase

from store.models import Product, Cart, CartLine


class TestModels(TestCase):
    
    def setUp(self):
        self.product1 = Product.objects.create(
            name='product1',
            category='category1',
            description='',
            price=10.00
        )
        self.product2 = Product.objects.create(
            name='product2',
            category='category2',
            description='',
            price=15.00
        )
        self.product3 = Product.objects.create(
            name='product3',
            category='category1',
            description='',
            price=2.35
        )
        self.cart = Cart()
        self.cart.lines = [
            CartLine(self.product1, 1),
            CartLine(self.product2, 2),
            CartLine(self.product3, 1),
        ]
        

    def test_Cart_class_total_price(self):
        self.assertEquals(self.cart.total_price, 42.35)


    def test_Cart_class_total_item_types(self):
        self.assertEquals(self.cart.total_item_types, 3)


    def test_Cart_class_total_items(self):
        self.assertEquals(self.cart.total_items, 4)


    def test_CartLine_add_amount_correct_data_type(self):
        cartLine = CartLine(self.product1, 2)
        cartLine.add_amount(1)
        self.assertEquals(cartLine.amount, 3)
    

    def test_CartLine_add_amount_wrong_data_type(self):
        cartLine = CartLine(self.product1, 2)
        cartLine.add_amount("1")
        self.assertEquals(cartLine.amount, 2)


    def test_CartLine_total_price(self):
        cartLine = CartLine(self.product1, 2)
        self.assertEquals(cartLine.total_price, 20.00)
    