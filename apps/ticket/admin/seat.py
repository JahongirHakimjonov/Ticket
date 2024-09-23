from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.ticket.models import Seat


@admin.register(Seat)
class SeatAdmin(ModelAdmin):
    list_display = ("id", "row", "seat_number", "hall", "created_at")
    search_fields = ("row", "seat_number", "hall__name")
    list_filter = ("created_at",)
    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Faol qilish"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Faol emas qilish"
