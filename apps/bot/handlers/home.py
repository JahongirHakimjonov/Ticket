from datetime import datetime

from telebot import TeleBot
from telebot.types import Message

from apps.bot.handlers.active_ticket import handle_active_tickets
from apps.bot.handlers.all_ticket import handle_all_tickets
from apps.bot.handlers.concert import handle_concert
from apps.bot.handlers.donate import handle_donate
from apps.bot.handlers.info import handle_info
from apps.bot.handlers.language import handle_language
from apps.bot.handlers.selection_date import handle_date_selection
from apps.bot.handlers.ticket import handle_ticket
from apps.bot.keyboard import get_main_buttons
from django.utils.translation import activate, gettext as _

from apps.bot.utils.language import set_language_code


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def handle_message(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    # state = bot.get_state(message.from_user.id, message.chat.id)
    if message.text == _("Concert"):
        handle_concert(message, bot)
    elif message.text == _("Donate"):
        handle_donate(message, bot)
    elif message.text == _("My Tickets"):
        handle_ticket(message, bot)
    elif message.text == _("Info"):
        handle_info(message, bot)
    elif message.text == _("Language"):
        handle_language(message, bot)
    elif message.text == _("All"):
        handle_date_selection(message, bot)
    elif message.text == _("All Tickets"):
        handle_all_tickets(message, bot)
    elif message.text == _("Active Tickets"):
        handle_active_tickets(message, bot)
    elif is_valid_date(message.text):
        handle_date_selection(message, bot)
    elif message.text == _("Home"):
        bot.send_message(
            message.chat.id,
            _("Welcome to the main menu!"),
            reply_markup=get_main_buttons(),
        )
    # elif state == Order.full_name:
    #     handle_full_name(message, bot)
    # elif state == Order.phone:
    #     handle_phone(message, bot)
    else:
        bot.send_message(
            message.chat.id,
            _("I don't understand you, please use the buttons below"),
            reply_markup=get_main_buttons(),
        )
