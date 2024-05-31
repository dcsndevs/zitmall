from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<slug:product_slug>/',
         views.product_detail_by_slug,
         name='product_detail_by_slug'),
]
