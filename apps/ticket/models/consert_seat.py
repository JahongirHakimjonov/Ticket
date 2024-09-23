from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class ConcertSeat(AbstractBaseModel):
    concert = models.ForeignKey(
        "Concert", on_delete=models.CASCADE, verbose_name=_("Konsert")
    )
    seat = models.ForeignKey("Seat", on_delete=models.CASCADE, verbose_name=_("Joy"))
    is_sold = models.BooleanField(default=False, verbose_name=_("Sotilganmi"))

    def __str__(self):
        return f"{self.concert} - {self.seat} - {self.is_sold}"

    class Meta:
        db_table = "concert_seat"
        verbose_name = _("Konsert joyi")
        verbose_name_plural = _("Konsert joylari")
