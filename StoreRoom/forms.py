from django import forms
from .models import ReviewAndRating, ProductCustomization

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = ReviewAndRating
        fields = ['subject', 'rating', 'review']
        
