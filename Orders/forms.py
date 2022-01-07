from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    imageForCustomization1 = forms.ImageField(required=False, error_messages={
                                      'invalid': ("Image Files Only")}, widget=forms.FileInput)
    
    imageForCustomization2 = forms.ImageField(required=False, error_messages={
                                      'invalid': ("Image Files Only")}, widget=forms.FileInput)
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'address_line_1',
            'address_line_2',
            'country',
            'state',
            'city',
            'pincode',
            'order_note',
            'paymentMethod',
            'imageForCustomization1',
            'imageForCustomization2'
            ]
