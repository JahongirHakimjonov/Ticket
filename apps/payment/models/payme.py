from django.db import models

from apps.payment.choices import (
    PaymentChoices,
    PaymentMethodChoices,
    PaymentTypeChoices,
)
from apps.shared.models import AbstractBaseModel


class Payment(AbstractBaseModel):
    order_id = models.CharField(max_length=255)
    status = models.CharField(
        choices=PaymentChoices.choices,
        default=PaymentChoices.PROCESSING,
        max_length=100,
    )
    transaction_id = models.CharField(max_length=255)
    payment_method = models.CharField(
        max_length=100,
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.PAYME,
    )
    type = models.CharField(max_length=100, choices=PaymentTypeChoices.choices)

    amount = models.IntegerField()
    message = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Order: {self.order_id}, Status: {self.status}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        db_table = "payment"
