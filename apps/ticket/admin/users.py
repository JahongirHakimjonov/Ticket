from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.ticket.models.users import BotUsers


@admin.register(BotUsers)
class BotUsersAdmin(ModelAdmin):
    list_display = (
        "id",
        "telegram_id",
        "username",
        "phone",
        "language_code",
        "is_active",
        "role",
    )
    list_filter = ("is_active", "role", "language_code")
    search_fields = ("first_name", "last_name", "phone", "username")
    ordering = ("-created_at",)
    list_editable = ("is_active", "role")
    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Faol qilish"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Faol emas qilish"
