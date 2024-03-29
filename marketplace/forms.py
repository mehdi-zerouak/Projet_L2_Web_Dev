from django import forms
from .models import Product

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['label', 'price', 'description','quantity','phone','image']
