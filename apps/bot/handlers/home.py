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


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def handle_message(message: Message, bot: TeleBot):
    # state = bot.get_state(message.from_user.id, message.chat.id)
    if message.text == "Concert":
        handle_concert(message, bot)
    elif message.text == "Donate":
        handle_donate(message, bot)
    elif message.text == "My Tickets":
        handle_ticket(message, bot)
    elif message.text == "Info":
        handle_info(message, bot)
    elif message.text == "Language":
        handle_language(message, bot)
    elif message.text == "All":
        handle_date_selection(message, bot)
    elif message.text == "All Tickets":
        handle_all_tickets(message, bot)
    elif message.text == "Active Tickets":
        handle_active_tickets(message, bot)
    elif is_valid_date(message.text):
        handle_date_selection(message, bot)
    elif message.text == "Home":
        bot.send_message(
            message.chat.id,
            "Welcome to the main menu!",
            reply_markup=get_main_buttons(),
        )
    # elif state == Order.full_name:
    #     handle_full_name(message, bot)
    # elif state == Order.phone:
    #     handle_phone(message, bot)
    else:
        bot.send_message(
            message.chat.id,
            "I don't understand you, please use the buttons below",
            reply_markup=get_main_buttons(),
        )
