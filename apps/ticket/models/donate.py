from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Donate(AbstractBaseModel):
    user = models.ForeignKey(
        "BotUsers", on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi")
    )
    amount = models.DecimalField(
        max_digits=100, decimal_places=2, verbose_name=_("Summa")
    )

    def __str__(self):
        return self.user

    class Meta:
        db_table = "donate"
        verbose_name = _("Xayriya")
        verbose_name_plural = _("Xayriyalar")
