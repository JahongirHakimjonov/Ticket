from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.ticket.filters import TicketConcertFilter
from apps.ticket.models.ticket import Ticket


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    """
    TicketAdmin class
    """

    list_display = ["id", "seat_id", "seat_number", "seat", "full_name", "is_active"]
    list_editable = ["is_active", "seat", "seat_number", "seat_id"]
    search_fields = ["ticket_id"]
    list_filter = ["is_active", TicketConcertFilter]
    list_filter_submit = True

    def full_name(self, obj):
        return obj.order.full_name
