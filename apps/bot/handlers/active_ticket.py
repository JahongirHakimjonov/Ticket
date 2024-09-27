from django.utils import timezone
from telebot import TeleBot
from telebot.types import Message

from apps.bot.logger import logger
from apps.bot.utils.language import set_language_code
from apps.ticket.models import Order, BotUsers
from django.utils.translation import activate, gettext as _


def handle_active_tickets(message: Message, bot: TeleBot):
    user = BotUsers.objects.get(telegram_id=message.from_user.id)
    activate(set_language_code(message.from_user.id))
    orders = Order.objects.filter(user_id=user.id, concert__date__gte=timezone.now())
    if not orders.exists():
        bot.send_message(message.chat.id, _("Sizda faol chiptalar mavjud emas."))
        return

    for order in orders:
        text = _(
            f"Order ID: {order.id}\nOrder Date: {order.concert.name}\nOrder Details: {order.total_price:,}\n"
        )
        bot.send_message(message.chat.id, text)
        logger.info(f"Active ticket sent to user {user.id}")
