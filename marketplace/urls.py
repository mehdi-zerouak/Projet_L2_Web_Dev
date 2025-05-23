# marketplace urls
from django.urls import path 
from marketplace import views

#for namespace
app_name = 'marketplace'

urlpatterns = [
    path('' , views.Products.as_view() , name = 'mp-home'),
    path('create/',views.CreateProduct.as_view(), name='mp-create'),
    path('product/<int:pk>/edit/',views.EditProduct.as_view(),name="mp-edit"),
    path('product/<int:pk>/',views.ProductDetails.as_view(), name='mp-details'),
    path('product/<int:pk>/delete/',views.DeleteProduct.as_view(),name='mp-delete'),
    path('search/',views.AnotherFilterView.as_view(),name="mp-search")
]