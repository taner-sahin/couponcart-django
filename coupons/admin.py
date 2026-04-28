from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percent", "active", "created_at")
    list_filter = ("active", "created_at")
    search_fields = ("code",)