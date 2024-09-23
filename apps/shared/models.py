from django.db import models

from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan vaqti"))
    is_active = models.BooleanField(default=True, verbose_name=_("Aktivmi"))

    class Meta:
        abstract = True
