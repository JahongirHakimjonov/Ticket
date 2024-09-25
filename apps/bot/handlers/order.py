
from telebot.types import Message
from telebot import TeleBot
from apps.bot.states.order_state import Order

def handle_full_name(message: Message, bot: TeleBot):
    full_name = message.text
    bot.send_message(
        message.chat.id, f"Rahmat, {full_name}. Endi telefon raqamingizni kiriting:"
    )
    bot.set_state(message.from_user.id, Order.phone, message.chat.id)

def handle_phone(message: Message, bot: TeleBot):
    phone = message.text
    bot.send_message(
        message.chat.id,
        f"Rahmat, telefon raqamingiz: {phone}. Buyurtmangiz qabul qilindi.",
    )
    bot.delete_state(message.from_user.id, message.chat.id)