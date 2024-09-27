from telebot import TeleBot
from telebot.types import Message

from apps.bot.states.order_state import Order
from django.utils.translation import activate, gettext as _

from apps.bot.utils.language import set_language_code


def handle_full_name(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    full_name = message.text
    bot.send_message(
        message.chat.id, _(f"Rahmat, {full_name}. Endi telefon raqamingizni kiriting:")
    )
    bot.set_state(message.from_user.id, Order.phone, message.chat.id)


def handle_phone(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    phone = message.text
    bot.send_message(
        message.chat.id,
        _(f"Rahmat, telefon raqamingiz: {phone}. Buyurtmangiz qabul qilindi."),
    )
    bot.delete_state(message.from_user.id, message.chat.id)
