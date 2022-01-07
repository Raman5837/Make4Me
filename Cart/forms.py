from django import forms
from StoreRoom.models import ProductCustomization

class ProductCustomization_Form(forms.ModelForm):
    
    class Meta:
        model = ProductCustomization
        fields = ['customizationImage', 'cutomizationNotes', 'product', 'user']
