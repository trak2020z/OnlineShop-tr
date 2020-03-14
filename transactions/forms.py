from django.forms import ModelForm
from django.forms import Form

from .models import Order, Ordered

class OrderForm(ModelForm):
    
    class Meta:
        model = Order
        fields = [
            'name',
            'surname',
            'email',
            'phone_number',
            'street_name',
            'zip_code',
            'city_name',
            'payment_type',
            'shipping_type',
        ]
    
    # W celu przpisania zalogowanego urzytkownika
    def custom_save(self, user, commit=True):
        order = super(OrderForm, self).save(commit=False)
        order.user = user
        # do custom stuff
        if commit:
            order.save()
        return order
