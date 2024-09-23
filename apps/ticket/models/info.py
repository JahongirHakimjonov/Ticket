from django.db import models

from apps.shared.models import AbstractBaseModel
from django.utils.translation import gettext_lazy as _


class Info(AbstractBaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Nomi"))
    description = models.TextField(verbose_name=_("Tavsif"))
    phone = models.CharField(max_length=255, verbose_name=_("Telefon raqam"))
    email = models.EmailField(verbose_name=_("Email"))
    location = models.URLField(max_length=255, verbose_name=_("Lokatsiya"))
    address = models.CharField(max_length=255, verbose_name=_("Manzil"))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "info"
        verbose_name = _("Ma'lumot")
        verbose_name_plural = _("Ma'lumotlar")
