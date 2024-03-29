from django.contrib import admin
from django.urls import path , include
# -- our urls
from blog import urls as blog_urls
from marketplace import urls as marketplace_urls
from users import urls as users_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(users_urls , namespace="user")),
    path('blog/', include(blog_urls , namespace="blog")),
    path('marketplace/', include(marketplace_urls , namespace="marketplace")),
]
