from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.ticket.filters import TicketConcertFilter
from apps.ticket.models.ticket import Ticket


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    """
    TicketAdmin class
    """

    list_display = ["id", "ticket_id", "created_at", "seat", "is_active"]
    list_editable = ["is_active"]
    search_fields = ["ticket_id"]
    list_filter = ["is_active", TicketConcertFilter]
    list_filter_submit = True
