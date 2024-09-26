from django.db import models

from apps.payment.choices import PaymentChoices, PaymentMethodChoices
from apps.ticket.models import Order


class Payment(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    amount = models.IntegerField()
    message = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Order: {self.order_id}, Status: {self.status}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        db_table = "payment"
