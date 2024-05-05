from django.contrib import admin
from .models import Product, Category


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'product_brand']
    list_display = (
        'id',
        'sku',
        'title',
        'category',
        'price',
        'image',
        'vendor',
        'product_brand',
        'status',
    )
    summernote_fields = ('description')

    ordering = ('-id',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)