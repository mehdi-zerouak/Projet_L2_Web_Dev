# users urls
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from users import views
from django.contrib.auth import views as auth_views

#for namespace
app_name = 'users'

urlpatterns = [
    # AUTH urls ------------------------------------------------------------------------------------------------------------
     path('' , views.home , name = 'u-home'),
     path('login/' , views.Login.as_view() , name = 'u-login'),
     path('logout/' , auth_views.LogoutView.as_view(next_page="user:u-home") , name = 'u-logout'),
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
                        # --------- friends stuff urls --------- 
     path('send-friend-request/<int:pk>' , views.send_friend_request , name="u-send-friend-request"),
     path('accept-friend-request/<int:pk>' , views.accept_friend_request , name='u-accept-friend-request'),
     path('remove-friend/<int:pk>' , views.remove_friend , name='u-remove-friend'),
     path('friend-requests-list/<str:username>' , views.friend_requests_list , name='u-friend-requests-list'),
     path('friends-list/<str:username>' , views.friends_list , name='u-friends-list'),
                        # --------------------------------------
     # ----------------------------------------------------------------------------------------------------------------------
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)