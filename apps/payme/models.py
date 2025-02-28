from django.db import models
from django.conf import settings
from django.utils.module_loading import import_string
from django.core.exceptions import FieldError
from django.utils.translation import gettext_lazy as _

from apps.payme.utils.logging import logger


class MerchantTransactionsModel(models.Model):
    """
    MerchantTransactionsModel class \
        That's used for managing transactions in database.
    """

    _id = models.CharField(max_length=255, null=True, blank=False)
    transaction_id = models.CharField(
        max_length=255, null=True, blank=False, verbose_name=_("Transaction ID")
    )
    order_id = models.CharField(
        max_length=300, null=True, blank=True, verbose_name=_("Order ID")
    )
    amount = models.FloatField(null=True, blank=True, verbose_name=_("Amount"))
    time = models.BigIntegerField(null=True, blank=True, verbose_name=_("Time"))
    perform_time = models.BigIntegerField(
        null=True, default=0, verbose_name=_("Perform Time")
    )
    cancel_time = models.BigIntegerField(
        null=True, default=0, verbose_name=_("Cancel Time")
    )
    state = models.IntegerField(null=True, default=1, verbose_name=_("State"))
    reason = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Reason")
    )
    created_at_ms = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Created At MS")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return str(self._id)

    class Meta:
        verbose_name = _("Merchant Transaction")
        verbose_name_plural = _("Merchant Transactions")


try:
    CUSTOM_ORDER = import_string(settings.ORDER_MODEL)

    if not isinstance(CUSTOM_ORDER, models.base.ModelBase):
        raise TypeError("The input must be an instance of models.Model class")

    # pylint: disable=protected-access
    if "amount" not in [f.name for f in CUSTOM_ORDER._meta.fields]:
        raise FieldError("Missing 'amount' field in your custom order model")

    Order = CUSTOM_ORDER
except (ImportError, AttributeError):
    logger.warning("You have no payme custom order model")

    CUSTOM_ORDER = None

    class Order(models.Model):
        """
        Order class \
            That's used for managing order process
        """

        amount = models.IntegerField(null=True, blank=True, verbose_name=_("Amount"))
        created_at = models.DateTimeField(
            auto_now_add=True, verbose_name=_("Created At")
        )
        updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

        def __str__(self):
            return f"ORDER ID: {self.pk} - AMOUNT: {self.amount}"

        class Meta:
            # pylint: disable=missing-class-docstring
            managed = False
            verbose_name = _("Order")
            verbose_name_plural = _("Orders")
