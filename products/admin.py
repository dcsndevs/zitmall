from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Product, Category


class ProductAdmin(SummernoteModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title", "sku"]
    list_display = (
        "id",
        "sku",
        "title",
        "category",
        "price",
        "vendor",
        "quantity",
        "status",
    )
    summernote_fields = "description"

    ordering = ("-id",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "friendly_name",
        "name",
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
