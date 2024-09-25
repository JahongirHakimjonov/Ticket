from django.utils import timezone
from telebot import TeleBot
from telebot.types import Message

from apps.bot.logger import logger
from apps.ticket.models import Order, BotUsers


def handle_active_tickets(message: Message, bot: TeleBot):
    user = BotUsers.objects.get(telegram_id=message.from_user.id)
    orders = Order.objects.filter(user_id=user.id, concert__date__gte=timezone.now())
    if not orders.exists():
        bot.send_message(message.chat.id, "Sizda faol chiptalar mavjud emas.")
        return

    for order in orders:
        text = (
            f"Order ID: {order.id}\n"
            f"Order Date: {order.concert.name}\n"
            f"Order Details: {order.total_price:,}\n"
        )
        bot.send_message(message.chat.id, text)
        logger.info(f"Active ticket sent to user {user.id}")
