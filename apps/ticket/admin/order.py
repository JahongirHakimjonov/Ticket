from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.ticket.models import Order


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ("id", "user", "total_price", "created_at")
    search_fields = ("user__username", "user__phone")
    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Faol qilish"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Faol emas qilish"
