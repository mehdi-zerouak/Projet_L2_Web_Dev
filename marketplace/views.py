# marketplace views
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Product,Category
from users.models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,DetailView,DeleteView,UpdateView,ListView,View
from .forms import CreateProductForm,SearchProductsForm
from django.db.models import Q
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
    


class FilterProducts(LoginRequiredMixin, View):
    def get(self, request):
        form = SearchProductsForm(request.GET)  # Create an instance of the form with GET data

        if form.is_valid():
            category = form.cleaned_data.get('category', '')  # Get the category from the form
            max_price = form.cleaned_data.get('max_price', 0)  # Get the max_price from the form
            name = form.cleaned_data.get('name', '')  # Get the name from the form
            filter_criteria = Q()  # Initialize an empty Q object for filtering

            if category:
                filter_criteria &= Q(category=category)

            if max_price:
                filter_criteria &= Q(price__lte=max_price)

            if name:
                filter_criteria &= (Q(label__icontains=name) | Q(description__icontains=name))

            filtered_products = Product.objects.filter(filter_criteria)  # Apply filters to the Product queryset
        else:
            # If form is not valid, handle accordingly
            filtered_products = Product.objects.none()

        return render(request, 'marketplace/search.html', {'filtered_products': filtered_products, 'form': form})