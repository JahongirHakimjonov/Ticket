from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class News(AbstractBaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Sarlavha"))
    content = models.TextField(verbose_name=_("Maqola"))
    image = models.ImageField(
        upload_to="news/", verbose_name=_("Rasm"), null=True, blank=True
    )

    class Meta:
        db_table = "news"
        verbose_name = _("Yangilik")
        verbose_name_plural = _("Yangiliklar")

    def __str__(self):
        return self.title
