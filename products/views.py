from django.shortcuts import render
from django.views.generic import ListView
from .models import Product

# Create your views here.
def all_products(request):
    
    return render(request, 'products/products.html')

class PostList(ListView):
    queryset = Product.objects.filter(status=1)
    template_name = "products/all-products.html"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_fields'] = ['image', 'image_2']  # Add all image fields here
        return context