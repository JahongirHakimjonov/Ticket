from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Seat(AbstractBaseModel):
    hall = models.ForeignKey("Hall", on_delete=models.CASCADE, verbose_name=_("Zal"))
    row = models.PositiveIntegerField(verbose_name=_("Qator"))
    seat_number = models.PositiveIntegerField(verbose_name=_("Joy raqami"))
    price = models.DecimalField(
        max_digits=100, decimal_places=2, verbose_name=_("Narx")
    )

    def __str__(self):
        return f"{self.hall} - {self.row} - {self.seat_number}"

    class Meta:
        db_table = "seat"
        verbose_name = _("Joy")
        verbose_name_plural = _("Joylar")
