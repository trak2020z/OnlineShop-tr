from django.db import models



# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=400)
    category = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    orders = models.ManyToManyField('transactions.Order', through='transactions.Ordered')

    def __str__(self):
        return self.name
    

    
# Wrapper class - w celu ułatwienia wyświetlania produktów na stronie
class Cart:
    def __init__(self):
        self.lines = []

    def add_to_cart(self, item, amount):
        for line in self.lines:
            if line.product == item:
                i = self.lines.index(line)
                self.lines[i].add_amount(amount)
                return
            
        self.lines.append(CartLine(item, amount))

    @property
    def total_price(self):
        return sum([line.total_price for line in self.lines])
    
    @property
    def total_item_types(self):
        return len(self.lines)
    
    @property
    def total_items(self):
        return sum([line.amount for line in self.lines])

# Klasa Zamówienia dla jednego produktu wykorzystywana w obiekcie klasy Cart
class CartLine:
    def __init__(self, product, amount):
        self.product = product
        self.amount = amount
    
    def add_amount(self, amount):
        if type(amount) == int:
            self.amount = self.amount + amount

    @property
    def total_price(self):
        return self.product.price * self.amount
