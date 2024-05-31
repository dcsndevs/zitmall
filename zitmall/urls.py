from django.contrib import admin
from django.urls import path, include
from zitmall.views import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('products/', include('products.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('profile/', include('profiles.urls')),
    path('vendor/', include('vendor.urls')),
    path('', include('home.urls')),
]

handler404 = handler404
handler500 = handler500

admin.site.site_header = "Admin | Zit Technology v1.0"
admin.site.site_title = "Admin | Zit Technology v1.0"
admin.site.index_title = ""
