import os

from django.utils import timezone
from django.utils.translation import activate, gettext as _
from telebot import TeleBot
from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    WebAppInfo,
    InlineKeyboardButton,
)

from apps.bot.logger import logger
from apps.bot.utils.language import set_language_code
from apps.ticket.models import BotUsers, Ticket


def handle_ticket(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    user = BotUsers.objects.get(telegram_id=message.from_user.id)
    orders = Ticket.objects.filter(
        order__user_id=user.id, order__concert__date__gte=timezone.now()
    )
    if not orders.exists():
        bot.send_message(message.chat.id, _("Sizda faol chiptalar mavjud emas."))
        return

    inline_markup = InlineKeyboardMarkup()

    if orders[0].order.seat.concert and orders[0].order.seat.concert.map:
        web_app = WebAppInfo(
            f"{os.getenv('BASE_URL')}{orders[0].order.seat.concert.map.url}"
        )
        inline_markup.add(
            InlineKeyboardButton(_("Sahna chizmasi"), web_app=web_app),
        )

    for order in orders:
        text = f"{order.seat}\n\nID: {order.ticket_id}"
        bot.send_document(
            message.chat.id, order.ticket, caption=text, reply_markup=inline_markup
        )
        logger.info(f"Active ticket sent to user {user.id}")
    # btn_active_tickets = types.KeyboardButton(_("Active Tickets"))
    # btn_all_tickets = types.KeyboardButton(_("All Tickets"))
    # btn_back = types.KeyboardButton(_("Home"))
    # keyboard.add(btn_active_tickets, btn_all_tickets, btn_back)

    # bot.send_message(
    #     message.chat.id, _("Kerakli bo'limni tanlang:"), reply_markup=keyboard
    # )
