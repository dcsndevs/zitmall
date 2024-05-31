from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_cart, name="view_cart"),
    path("add/<item_id>/", views.add_to_cart, name="add_to_cart"),
    path("adjust/<item_id>/", views.adjust_cart, name="adjust_cart"),
    path("remove/<item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("apply_coupon", views.apply_coupon, name="apply_coupon"),
    path("quick_add/<int:item_id>/", views.quick_add_to_cart,
         name="quick_add_to_cart"),
    path("empty_cart", views.empty_cart, name="empty_cart"),
]
