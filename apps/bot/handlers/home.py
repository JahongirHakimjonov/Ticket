from telebot import TeleBot
from telebot.types import Message

from apps.bot.buttons import get_main_buttons
from apps.bot.handlers.concert import handle_concert
from apps.bot.handlers.donate import handle_donate
from apps.bot.handlers.info import handle_info
from apps.bot.handlers.language import handle_language
from apps.bot.handlers.ticket import handle_ticket


def handle_message(message: Message, bot: TeleBot):
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
    else:
        bot.send_message(
            message.chat.id,
            "Please select an option from the menu.",
            reply_markup=get_main_buttons(),
        )
