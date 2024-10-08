from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin, TabularInline

from apps.ticket.filters import ConcertFilter
from apps.ticket.models import Seat, SeatNumber


class SeatNumberInline(TabularInline):
    model = SeatNumber
    fields = ("number", "is_active")


@admin.register(Seat)
class SeatAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name", "count", "price", "concert", "is_active", "type")
    search_fields = ("name",)
    list_filter = (ConcertFilter, "is_active")
    list_editable = ("name", "count", "price", "is_active", "type")
    actions = ["make_active", "make_inactive"]
    list_filter_submit = True
    inlines = [SeatNumberInline]

    def make_active(self, request, queryset):  # noqa
        queryset.update(is_active=True)

    make_active.short_description = "Faol qilish"

    def make_inactive(self, request, queryset):  # noqa
        queryset.update(is_active=False)

    make_inactive.short_description = "Faol emas qilish"
