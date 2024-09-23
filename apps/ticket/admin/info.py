from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.ticket.models import Info


@admin.register(Info)
class InfoAdmin(ModelAdmin):
    list_display = ("id", "name", "created_at")
    list_filter = ("created_at",)
    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Faol qilish"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Faol emas qilish"
