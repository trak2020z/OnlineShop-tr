from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from enum import Enum
import uuid

from store.models import Product

PHONE_NUMBER_VALIDATOR = RegexValidator(r'^[0-9]*$', 'Only numbers allowed')
ZIP_CODE_VALIDATOR = RegexValidator(r'^[\d]{2}-[\d]{3}$')

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(
        'store.Product', 
        through='Ordered'
    )
    date = models.DateTimeField(auto_now=True, editable=False)
    access_code = models.UUIDField(unique=True, editable=False, 
        default=uuid.uuid4)
    
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=350)
    phone_number = models.CharField(max_length=9, 
        validators=[PHONE_NUMBER_VALIDATOR])

    street_name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6, 
        validators=[ZIP_CODE_VALIDATOR])
    
    city_name = models.CharField(max_length=100)

    total_price = models.DecimalField(max_digits=7, 
        decimal_places=2, default=0)
    
    is_paid = models.BooleanField(default=False)

    class PAYMENTS(Enum):
        card = (1, 'Card')
        blik = (2, 'Blik')
        transfer = (3, 'Transfer')
        paypal = (4, 'Paypal')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]
        
        @classmethod
        def get_text(cls, member):
            return cls[member].value[1]
    
    class SHIPPING(Enum):
        post = (1, 'Post')
        courier = (2, 'Courier')
        parcel_locker = (3, 'Parcel locker')
        pick_up = (4, 'Own pickup')
        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]
        @classmethod
        def get_text(cls, member):
            return cls[member].value[1]
    payment_type = models.PositiveIntegerField(
        choices=[x.value for x in PAYMENTS] )
    shipping_type = models.PositiveIntegerField(
        choices=[x.value for x in SHIPPING] )
    
    def __str__(self):
        return '{} - {} {}'.format(self.date, self.name, self.surname)

# Klasa pośrednicząca między Zamówieniem i produktem
class Ordered(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1, )

    def __str__(self):
        return '{} {}'.format(self.order.id, self.product.name)
    