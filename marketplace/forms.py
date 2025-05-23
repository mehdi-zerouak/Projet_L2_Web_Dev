from django import forms
from .models import Product,Category

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['label', 'price', 'description','quantity','phone','image' , 'category']
        
class SearchProductsForm(forms.Form):
    name = forms.CharField(max_length=100,required=False )
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select category" , required=False )
    max_price = forms.IntegerField(min_value=0, label='Maximum Price' )
    