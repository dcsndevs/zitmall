from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('vendor/signup', views.vendor_signup, name='vendor_signup'),
]
