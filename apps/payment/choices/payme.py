from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentChoices(models.TextChoices):
    PROCESSING = "PROCESSING", _("Processing")
    COMPLETED = "COMPLETED", _("Completed")
    FAILED = "FAILED", _("Failed")
    CANCELLED = "CANCELLED", _("Cancelled")


class PaymentMethodChoices(models.TextChoices):
    CLICK = "CLICK", _("Click")
    PAYME = "PAYME", _("Payme")
    OCTO = "OCTO", _("OCTO")
    CASH = "CASH", _("Cash")


class PaymentTypeChoices(models.TextChoices):
    DONATE = "DONATE", _("Donate")
    ORDER = "ORDER", _("Order")
