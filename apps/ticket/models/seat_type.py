from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class SeatType(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "seat_type"
        verbose_name = _("Joy turi")
        verbose_name_plural = _("Joy turlari")
