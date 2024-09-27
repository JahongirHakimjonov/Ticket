# apps/payment/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.payme.models import MerchantTransactionsModel
from apps.payment.choices import PaymentChoices
from apps.payment.models import Payment
from apps.ticket.models import Donate, Order


@receiver(post_save, sender=MerchantTransactionsModel)
def check_payme_status(sender, instance, **kwargs):
    if instance.state == int(1):
        payment = Payment.objects.get(order_id=instance.order_id)
        payment.status = PaymentChoices.COMPLETED
        payment.save()


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


@receiver(post_save, sender=Order)
def check_order_status(sender, instance, **kwargs):
    if instance.is_paid:
        instance.seat.count -= instance.count
        instance.seat.save()
