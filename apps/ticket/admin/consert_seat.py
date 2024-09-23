from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.ticket.models import ConcertSeat


@admin.register(ConcertSeat)
class ConcertSeatAdmin(ModelAdmin):
    list_display = ("id", "concert", "seat", "is_active")
    search_fields = ("concert__name",)
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Faol qilish"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Faol emas qilish"
