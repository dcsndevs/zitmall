from django.contrib import admin
from .models import VendorOrder


class VendorOrderAdmin(admin.ModelAdmin):
    search_fields = ["item"]
    list_display = ("id", "item", "fulfilment", "status", "reason")
    ordering = ("-id",)


admin.site.register(VendorOrder, VendorOrderAdmin)
