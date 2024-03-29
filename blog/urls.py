# blog urls
from django.urls import path 
from blog import views


#for namespace
app_name = 'blog'

urlpatterns = [
    path('' , views.home , name = 'b-home'),
    path('post/<int:pk>' , views.detail_post , name = 'b-post'), # detail page + add comment form
    path('create-post/' , views.CreatePost.as_view() , name = 'b-create-post'),
    path('update-post/<int:pk>' , views.UpdatePost.as_view() , name = 'b-update-post'),
    path('delete-post/<int:pk>' , views.delete_post , name = 'b-delete-post'),
    path('delete-comment/<int:pk>' , views.delete_comment , name = 'b-delete-comment'),
    path('post/<int:pk>/like/' , views.like_post , name = 'b-like-post'),
]