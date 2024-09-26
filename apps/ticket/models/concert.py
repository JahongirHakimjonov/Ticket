from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Concert(AbstractBaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Nomi"))
    title = models.CharField(max_length=255, verbose_name=_("Sarlavha"))
    description = models.TextField(verbose_name=_("Tavsif"))
    date = models.DateField(verbose_name=_("Sanasi"))
    time = models.TimeField(verbose_name=_("Vaqt"))
    min_price = models.DecimalField(
        max_digits=100, decimal_places=2, verbose_name=_("Eng arzon narx")
    )
    max_price = models.DecimalField(
        max_digits=100, decimal_places=2, verbose_name=_("Eng qimmat narx")
    )
    address = models.CharField(max_length=255, verbose_name=_("Manzil"))
    location_google_maps = models.URLField(
        max_length=255, verbose_name=_("Google Maps manzili")
    )
    location_yandex_maps = models.URLField(
        max_length=255, verbose_name=_("Yandex Maps manzili")
    )
    photo = models.ImageField(
        upload_to="concerts",
        verbose_name=_("Rasm"),
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"])],
    )
    thumbnail = models.ImageField(
        upload_to="concerts/thumbnail",
        verbose_name=_("Mini rasm"),
        blank=True,
        null=True,
    )

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
        image.thumbnail((200, 200))
        thumb_name = self.photo.name.replace(".", "_thumb.")
        thumb_io = BytesIO()
        image.save(thumb_io, "JPEG", quality=85)
        self.thumbnail.save(thumb_name, ContentFile(thumb_io.getvalue()), save=False)
        thumb_io.close()
