from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class SeatNumber(AbstractBaseModel):
    seat = models.ForeignKey(
        "Seat", on_delete=models.CASCADE, related_name="seat_number"
    )
    number = models.CharField(max_length=10)

    def __str__(self):
        return self.number

    class Meta:
        db_table = "seat_number"
        verbose_name = _("O'rindiq raqami")
        verbose_name_plural = _("O'rindiq raqamlar")
