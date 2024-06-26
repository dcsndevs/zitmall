from django.contrib import admin
from .models import Coupon


class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount", "used", "usage_limit", "valid_to",
                    "active")
    list_filter = ("active", "valid_from", "valid_to")
    search_fields = ("code",)


admin.site.register(Coupon, CouponAdmin)
