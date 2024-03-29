# marketplace views
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Product
from users.models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,DetailView,DeleteView,UpdateView,ListView
from .forms import CreateProductForm

# Create your views here.
class Products(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'marketplace/index.html' 
    context_object_name = 'products' 


class ProductDetails(LoginRequiredMixin,DeleteView):
    model = Product
    template_name = "marketplace/product_detail.html"
    context_object_name = 'product'


class CreateProduct(LoginRequiredMixin,CreateView):
    model = Product
    form_class = CreateProductForm
    template_name = "marketplace/create_product.html"
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self) -> str:
        return reverse_lazy('marketplace:mp-home')
    

class EditProduct(LoginRequiredMixin,UpdateView):
    model = Product
    form_class = CreateProductForm
    template_name = "marketplace/edit_product.html"
    
    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user)
        return queryset
    
    def get_success_url(self):
        return reverse_lazy("marketplace:mp-details",kwargs={"pk":self.object.pk})
    
class DeleteProduct(LoginRequiredMixin,DeleteView):
    model = Product
    template_name = "marketplace/delete_product.html"
    context_object_name = "product"

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user)

        return queryset
    def get_success_url(self):
        return reverse_lazy("marketplace:mp-home")