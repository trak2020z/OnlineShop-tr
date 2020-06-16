from django import forms

from .models import Order, Ordered

class OrderForm(forms.ModelForm):
    
    # name = forms.CharField(max_length=100, error_messages={
    #     'required': 'Enter your name'
    # })
    # surname = forms.CharField(max_length=100, error_messages={
    #     'required': 'Enter your surname'
    # })
    email = forms.EmailField(max_length=350, error_messages={
        'required': 'Enter your email address',
        'invalid': 'Enter valid email address, example: email@example.com'
    })
    phone_number = forms.CharField(max_length=9, error_messages={
        'required': 'Enter your phone number',
        'invalid': 'Enter valid phone number - example 123456789'
    })
    # street_name = forms.CharField(max_length=100, error_messages={
    #     'required': 'Enter your street name',
    # })
    zip_code = forms.CharField(max_length=6, error_messages={
        'required': 'Enter your street name',
        'invalid': 'Enter valid value for example: 00-000'
    })
    # city_name = forms.CharField(max_length=100, error_messages={
    #     'required': 'Enter your street name',
    # })

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
