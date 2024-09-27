from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import DropdownFilter

from apps.ticket.models import Concert


class ConcertFilter(DropdownFilter):
    title = _("Konsertlar")
    parameter_name = "concert"

    def lookups(self, request, model_admin):
        concerts = Concert.objects.filter(is_active=True)
        return [
            (
                concert.id,
                f"{concert.name} - {concert.date.strftime('%d.%m.%Y')}",
            )
            for concert in concerts
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(concert__id=self.value())
        return queryset


class TicketConcertFilter(DropdownFilter):
    title = _("Konsertlar")
    parameter_name = "concert"

    def lookups(self, request, model_admin):
        concerts = Concert.objects.filter(is_active=True)
        return [
            (
                concert.id,
                f"{concert.name} - {concert.date.strftime('%d.%m.%Y')}",
            )
            for concert in concerts
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(order__concert__id=self.value())
        return queryset
