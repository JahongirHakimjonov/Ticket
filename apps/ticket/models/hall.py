from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Hall(AbstractBaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Nomi"))
    capacity = models.PositiveIntegerField(verbose_name=_("O'tish joyi"))
    location = models.URLField(max_length=255, verbose_name=_("Lokatsiya"))
    address = models.CharField(max_length=255, verbose_name=_("Manzil"))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "hall"
        verbose_name = _("Zal")
        verbose_name_plural = _("Zallar")
