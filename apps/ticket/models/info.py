from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Info(AbstractBaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Nomi"))
    description = models.TextField(verbose_name=_("Tavsif"))
    phone = models.CharField(max_length=255, verbose_name=_("Telefon raqam"))
    username = models.CharField(max_length=255, verbose_name=_("Telegram username"))
    email = models.EmailField(verbose_name=_("Email"))
    location = models.URLField(max_length=255, verbose_name=_("Lokatsiya"))
    address = models.CharField(max_length=255, verbose_name=_("Manzil"))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "info"
        verbose_name = _("Ma'lumot")
        verbose_name_plural = _("Ma'lumotlar")
