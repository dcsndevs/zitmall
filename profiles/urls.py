from django.urls import path
from . import views

urlpatterns = [    
    path('', views.view, name='profile_view'),
    path('change-password/', views.PasswordsChangeView.as_view(template_name='profiles/password_change.html'), name='password_change'),
    path('view/', views.profile, name='profile_address'),
    path('persona/', views.persona.as_view(), name='persona'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
]