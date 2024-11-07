from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.ticket.models.users import BotUsers


@admin.register(BotUsers)
class BotUsersAdmin(ModelAdmin):
    list_display = (
        "id",
        "telegram_id",
        "username",
        "full_name",
        "phone",
        "language_code",
        "is_active",
    )
    list_filter = ("is_active", "role", "language_code")
    search_fields = ("first_name", "last_name", "phone", "username", "telegram_id","full_name")
    ordering = ("-created_at",)
    actions = ["make_active", "make_inactive"]
    list_filter_submit = True

    def make_active(self, request, queryset):  # noqa
        queryset.update(is_active=True)

    make_active.short_description = "Faol qilish"

    def make_inactive(self, request, queryset):  # noqa
        queryset.update(is_active=False)

    make_inactive.short_description = "Faol emas qilish"
