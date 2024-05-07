from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_admin, name='vendor_admin'),
    path('add/', views.add_product, name='add_product'),
    path('products/', views.all_products, name='vendor_products'),
    path('products/<int:product_id>/<int:product_status>/', views.status_products, name='status_products'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('orders/', views.vendor_orders, name='vendor_orders'),
    path('orders/<str:order_no>/<int:orderline_id>/', views.vendor_order_view, name='vendor_order_view'),
    path('orders/<int:item_id>/accept', views.accept_order, name='accept_order'),
    path('orders/<int:item_id>/reject', views.reject_order, name='reject_order'),
    
    
]