from telebot import TeleBot, types
from telebot.types import Message
from django.utils.translation import activate, gettext as _

from apps.bot.utils.language import set_language_code


def handle_ticket(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_active_tickets = types.KeyboardButton(_("Active Tickets"))
    btn_all_tickets = types.KeyboardButton(_("All Tickets"))
    btn_back = types.KeyboardButton(_("Home"))
    keyboard.add(btn_active_tickets, btn_all_tickets, btn_back)

    bot.send_message(
        message.chat.id, _("Kerakli bo'limni tanlang:"), reply_markup=keyboard
    )
