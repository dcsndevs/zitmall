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
    path('orders/new', views.new_vendor_orders, name='new_vendor_orders'),
    path('orders/cancelled', views.cancelled_vendor_orders, name='cancelled_vendor_orders'),
    path('orders/delivered', views.delivered_vendor_orders, name='delivered_vendor_orders'),
    path('orders/delivery_failed', views.delivery_failed_vendor_orders, name='delivery_failed_vendor_orders'),
    path('orders/<str:order_no>/<int:orderline_id>/', views.vendor_order_view, name='vendor_order_view'),
    path('orders/active', views.active_vendor_orders, name='active_vendor_orders'),
    path('orders/<str:order_number>/<int:product_id>/zit', views.shipment_type, name='shipment_type'),
    path('orders/<str:order_number>/<int:product_id>/accept', views.accept_order, name='accept_order'),
    path('orders/<str:order_number>/<int:product_id>/reject', views.reject_order, name='reject_order'),    
    path('orders/<str:order_number>/<int:product_id>/<int:reason_value>/cancel', views.cancel_order, name='cancel_order'),
    path('orders/<str:order_number>/<int:product_id>/ship', views.ship_order, name='ship_order'),
    path('orders/<str:order_number>/<int:product_id>/deliver', views.deliver_order, name='deliver_order'),
    path('orders/<str:order_number>/<int:product_id>/delivery_failed', views.delivery_failed_order, name='delivery_failed_order'),
]