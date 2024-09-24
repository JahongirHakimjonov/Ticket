from telebot import TeleBot
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    Message,
)

from apps.ticket.models import Concert  # Import the Concert model


def handle_concert(message: Message, bot: TeleBot):
    # Inline button
    inline_markup = InlineKeyboardMarkup()
    inline_button = InlineKeyboardButton("Search Concerts", switch_inline_query_current_chat="")
    inline_markup.add(inline_button)

    # Fetch concert dates from the Concert model
    concert_dates = Concert.objects.filter(is_active=True).values_list('date', flat=True)

    # Keyboard button
    keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for date in concert_dates:
        keyboard_button = KeyboardButton(str(date))
        keyboard_markup.add(keyboard_button)

    bot.send_message(
        message.chat.id,
        "Please select a concert date or search for concerts:",
        reply_markup=inline_markup
    )
    bot.send_message(
        message.chat.id,
        "Available concert dates:",
        reply_markup=keyboard_markup
    )
