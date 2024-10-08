from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.ticket.models import SeatNumber


@admin.register(SeatNumber)
class SeatNumberAdmin(ModelAdmin):
    list_display = ("id", "seat", "number", "is_active")
    search_fields = ("number", "seat__name")
    list_filter = ("seat",)
    list_editable = ("seat", "number", "is_active")
