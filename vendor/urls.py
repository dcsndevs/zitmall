from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_admin, name='vendor_admin'),
    path('add/', views.add_product, name='add_product'),
    path('products/', views.all_products, name='vendor_products'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    
]