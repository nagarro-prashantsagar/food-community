# urls.py
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('custom-user/signup/', CustomUserSignupView.as_view(), name='custom_user_signup'),
    path('custom-user/login/', CustomUserLoginView.as_view(), name='custom_user_login'),
    path('custom-user/logout/', CustomUserLogoutView.as_view(), name='custom_user_logout'),

    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('admin/logout/', AdminLogoutView.as_view(), name='admin_logout'),

]
