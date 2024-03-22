# users urls
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # AUTH urls ------------------------------------------------------------------------------------------------------------
     path('' , views.home , name = 'u-home'),
     path('login/' , views.Login.as_view() , name = 'u-login'),
     path('logout/' , auth_views.LogoutView.as_view(next_page="u-home") , name = 'u-logout'),
     path('register/' , views.Register.as_view() , name='u-register'),
               # --------- password reset urls ---------
     path('password-reset/', views.custom_password_reset ,name='password_reset'),
     path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password-reset-done.html'),
         name='password_reset_done'),
     path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password-reset-confirm.html'),
         name='password_reset_confirm'),
     path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password-reset-complete.html') , 
         name="password_reset_complete"),
               # ----------------------------------------
     # ----------------------------------------------------------------------------------------------------------------------
     # PROFILE urls ---------------------------------------------------------------------------------------------------------
     path('profile/<str:username>' , views.profile , name='u-profile'),
     path('update-profile/<int:pk>' , views.UpdateProfile.as_view() , name='u-update-profile'),
     # ----------------------------------------------------------------------------------------------------------------------

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)