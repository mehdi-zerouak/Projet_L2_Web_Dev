# blog urls
from django.urls import path 
from blog import views

urlpatterns = [
    path('' , views.home , name = 'b-home'),
]