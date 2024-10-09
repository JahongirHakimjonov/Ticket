# apps/payment/signals.py
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.payme.models import MerchantTransactionsModel
from apps.payment.choices import PaymentChoices
from apps.payment.models import Payment
from apps.ticket.models import News
from apps.ticket.models import Order
from apps.ticket.models import Seat, SeatNumber
from apps.ticket.utils import send_news_to_subscribers


@receiver(m2m_changed, sender=Order.seat_numbers.through)
def seat_numbers_changed(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        # Recalculate the total price
        instance.total_price = sum(
            seat_number.seat.price for seat_number in instance.seat_numbers.all()
        )
        instance.count = instance.seat_numbers.count()
        instance.save()


@receiver(post_save, sender=MerchantTransactionsModel)
def check_payme_status(sender, instance, **kwargs):
    payment = Payment.objects.get(order_id=instance.order_id)
    payment.transaction_id = instance.transaction_id
    payment.save()
    if instance.state == int(2):
        payment.status = PaymentChoices.COMPLETED
        payment.save()
    elif instance.state == -1:
        payment.status = PaymentChoices.FAILED
        payment.save()
    elif instance.state == -2:
        payment.status = PaymentChoices.CANCELLED
        payment.save()


# @receiver(post_save, sender=Payment)
# def check_payment_status(sender, instance, **kwargs):
#     if instance.status == PaymentChoices.COMPLETED:
#         order_id = instance.order_id
#         if order_id.startswith("donate_"):
#             donate_id = int(order_id.split("_")[-1])
#             donate = Donate.objects.get(id=donate_id)
#             if donate:
#                 donate.is_paid = True
#                 donate.save()
#         elif order_id.startswith("order_"):
#             order_id = int(order_id.split("_")[-1])
#             order = Order.objects.get(id=order_id)
#             if order.seat.count < order.count:
#                 print("Not enough seats")
#                 message = f"Kechirasiz, {order.seat.count} ta bilet qoldi. Buyurtma bekor qilindi, noqulaylik uchun uzr so'raymiz\n\nИзвините, осталось билетов: {order.seat.count}. Заказ отменен, извините за неудобства"
#                 send_message(order_id, message)
#                 print("Message sent")
#             else:
#                 order.is_paid = True
#                 order.save()
#                 from apps.bot.utils.send_message import send_telegram_message
#
#                 send_telegram_message(order_id)
#                 generate_ticket_qr_code.delay(order_id)

#
# @receiver(post_save, sender=Order)
# def check_order_status(sender, instance, **kwargs):
#     if instance.is_paid:
#         instance.seat.count -= instance.count
#         instance.seat.save()


@receiver(post_save, sender=News)
def check_news_status(sender, instance, created, **kwargs):
    if created:
        send_news_to_subscribers.delay(instance.id)


@receiver(post_save, sender=Seat)
def create_seat_numbers(sender, instance, created, **kwargs):
    if created:
        for i in range(1, instance.count + 1):
            SeatNumber.objects.create(seat=instance, number=i)
