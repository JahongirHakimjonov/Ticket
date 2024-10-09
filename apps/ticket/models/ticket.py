from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Ticket(AbstractBaseModel):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="tickets")
    ticket_id = models.CharField(max_length=255, null=True, blank=False)
    ticket_id_url = models.URLField(max_length=255, null=True, blank=True)
    ticket = models.ImageField(upload_to="tickets/")
    seat = models.CharField(max_length=255, null=True, blank=False)
    seat_id = models.ForeignKey(
        "Seat", on_delete=models.CASCADE, verbose_name=_("Joy"), null=True, blank=True
    )
    seat_number = models.ForeignKey(
        "SeatNumber",
        on_delete=models.CASCADE,
        verbose_name=_("O'rindiq raqami"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Ticket {self.ticket_id} for Order {self.order.id}"

    class Meta:
        db_table = "ticket"
        verbose_name = _("Bilet")
        verbose_name_plural = _("Biletlar")
