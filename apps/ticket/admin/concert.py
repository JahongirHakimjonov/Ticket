from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin
from unfold.admin import TabularInline

from apps.ticket.models import Concert
from apps.ticket.models import Seat


class SeatInline(TabularInline):
    model = Seat
    fields = ("is_active", "name_uz", "", "count", "price")
    extra = 1


@admin.register(Concert)
class ConcertAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name", "date", "is_active")
    search_fields = ("name", "title", "description")
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    actions = ["make_active", "make_inactive"]
    inlines = [SeatInline]
    exclude = ("thumbnail",)

    def make_active(self, request, queryset):  # noqa
        queryset.update(is_active=True)

    make_active.short_description = "Faol qilish"

    def make_inactive(self, request, queryset):  # noqa
        queryset.update(is_active=False)

    make_inactive.short_description = "Faol emas qilish"
