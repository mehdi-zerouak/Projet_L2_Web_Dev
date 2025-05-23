# marketplace views
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Product
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,DeleteView,UpdateView,ListView,View
from .forms import CreateProductForm,SearchProductsForm
from django.db.models import Q

# Create your views here.
class Products(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'marketplace/index.html' 
    context_object_name = 'products' 
    ordering = ['-created_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchProductsForm()
        return context
    

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_object() 
        return context
    
class DeleteProduct(LoginRequiredMixin,DeleteView):
    model = Product
    template_name = "marketplace/delete_product.html"
    context_object_name = "product"

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user)

        return queryset
    def get_success_url(self):
        return reverse_lazy("marketplace:mp-home")
    
  

class AnotherFilterView(LoginRequiredMixin , View):
    def get(self , request):
        category = request.GET['category']
        max_price = request.GET['max_price']
        name = request.GET['name']
        filter_criteria = Q() 

        if category:
            filter_criteria &= Q(category=category)

        if max_price:
                filter_criteria &= Q(price__lte=max_price)

        if name:
                filter_criteria &= (Q(label__icontains=name) | Q(description__icontains=name))

        filtered_products = Product.objects.filter(filter_criteria)  # Apply filters to the Product queryset

        form = SearchProductsForm()
        return render(request, 'marketplace/index.html', {'products': filtered_products, 'form': form})