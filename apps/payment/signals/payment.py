# apps/payment/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.payment.choices import PaymentChoices
from apps.payment.models import Payment
from apps.ticket.models import Donate, Order


@receiver(post_save, sender=Payment)
def check_payment_status(sender, instance, **kwargs):
    if instance.status == PaymentChoices.COMPLETED:
        order_id = instance.order_id
        if order_id.startswith("donate_"):
            donate_id = int(order_id.split("_")[-1])
            donate = Donate.objects.get(id=donate_id)
            if donate:
                donate.is_paid = True
                donate.save()
        elif order_id.startswith("order_"):
            order_id = int(order_id.split("_")[-1])
            order = Order.objects.get(id=order_id)
            if order:
                order.is_paid = True
                order.save()
