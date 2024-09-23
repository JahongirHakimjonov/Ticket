from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from apps.bot.utils import update_or_create_user


def any_user(message: Message, bot: TeleBot):
    markup = InlineKeyboardMarkup()
    uz_button = InlineKeyboardButton("O'zbek", callback_data='uz')
    ru_button = InlineKeyboardButton('Русский', callback_data='ru')
    markup.add(uz_button, ru_button)
    bot.send_message(message.chat.id, "Tilni tanlang / Выберите язык", reply_markup=markup)
    bot.register_callback_query_handler(lambda call: save_user_language(call, bot),
                                        func=lambda call: call.data in ['uz', 'ru'])


def save_user_language(call, bot: TeleBot):
    language = call.data
    update_or_create_user(
        telegram_id=call.message.chat.id,
        username=call.from_user.username if call.from_user.username else None,
        first_name=call.from_user.first_name if call.from_user.first_name else None,
        last_name=call.from_user.last_name if call.from_user.last_name else None,
        phone=None,  # Assuming phone number is not available in the message
        language_code=language
    )
    bot.send_message(call.message.chat.id, "Til tanlandi / Язык выбран")
