from telebot import TeleBot, types
from telebot.types import Message, CallbackQuery

from apps.bot.logger import logger
from apps.ticket.models import BotUsers


def handle_language(message: Message, bot: TeleBot):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    # Create buttons for Russian and Uzbek languages
    ru_button = types.InlineKeyboardButton(text="Русский", callback_data="lang_ru")
    uz_button = types.InlineKeyboardButton(text="O'zbek", callback_data="lang_uz")

    # Add buttons to the keyboard
    keyboard.add(ru_button, uz_button)

    bot.send_message(
        message.chat.id, "Tilni tanlang / Выберите язык:", reply_markup=keyboard
    )


def handle_language_selection(call: CallbackQuery, bot: TeleBot):
    user = BotUsers.objects.get(telegram_id=call.from_user.id)
    logger.info(f"User {user.telegram_id} selected a language.")
    if call.data == "lang_ru":
        user.language_code = "ru"
    elif call.data == "lang_uz":
        user.language_code = "uz"
    user.save()
    bot.send_message(call.message.chat.id, "Language updated successfully!")
    bot.delete_message(call.message.chat.id, call.message.message_id)
