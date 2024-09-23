from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Concert(AbstractBaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Nomi"))
    title = models.CharField(max_length=255, verbose_name=_("Sarlavha"))
    description = models.TextField(verbose_name=_("Tavsif"))
    date = models.DateField(verbose_name=_("Boshlanish sanasi"))
    time = models.TimeField(verbose_name=_("Vaqt"))
    min_price = models.DecimalField(
        max_digits=100, decimal_places=2, verbose_name=_("Eng arzon narx")
    )
    max_price = models.DecimalField(
        max_digits=100, decimal_places=2, verbose_name=_("Eng qimmat narx")
    )
    hall = models.ForeignKey(
        "Hall", on_delete=models.CASCADE, verbose_name=_("Konsert zal")
    )
    photo = models.ImageField(upload_to="concerts", verbose_name=_("Rasm"))
    thumbnail = models.ImageField(upload_to="concerts", verbose_name=_("Mini rasm"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "concert"
        verbose_name = _("Konsert")
        verbose_name_plural = _("Konsertlar")

    def save(self, *args, **kwargs):
        if self.photo and not self.thumbnail:
            self.make_thumbnail()
        super().save(*args, **kwargs)

    def make_thumbnail(self):
        image = Image.open(self.photo)
        image.thumbnail((100, 100), Image.LANCZOS)

        thumb_io = BytesIO()
        image.save(thumb_io, format='JPEG', quality=85)

        thumb_file = ContentFile(thumb_io.getvalue(), name=self.photo.name)
        self.thumbnail.save(thumb_file.name, thumb_file, save=False)
