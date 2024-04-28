from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('all', views.PostList.as_view(), name='all-products'),
    
]