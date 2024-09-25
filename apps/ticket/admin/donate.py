from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.ticket.models import Donate


@admin.register(Donate)
class DonateAdmin(ModelAdmin):
    list_display = ("id", "user", "amount", "created_at")
    search_fields = ("user__username", "user__phone")
    list_filter = ("created_at",)
    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):  # noqa
        queryset.update(is_active=True)

    make_active.short_description = "Faol qilish"

    def make_inactive(self, request, queryset):  # noqa
        queryset.update(is_active=False)

    make_inactive.short_description = "Faol emas qilish"
