# marketplace urls
from django.urls import path 
from marketplace import views

urlpatterns = [
    path('' , views.home , name = 'mp-home'),
]