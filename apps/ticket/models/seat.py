from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Seat(AbstractBaseModel):
    type = models.ForeignKey(
        "SeatType",
        on_delete=models.CASCADE,
        verbose_name=_("Joy turi"),
        null=True,
        blank=True,
    )
    concert = models.ForeignKey("Concert", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    count = models.PositiveIntegerField(verbose_name=_("Joylar soni"))
    price = models.DecimalField(
        max_digits=100, decimal_places=2, verbose_name=_("Narx")
    )

    def __str__(self):
        return f"{self.name} - {self.concert.name}"

    class Meta:
        db_table = "seat"
        verbose_name = _("Joy")
        verbose_name_plural = _("Joylar")
