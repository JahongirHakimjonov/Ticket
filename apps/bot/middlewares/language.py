from django.utils.translation import activate
from telebot import TeleBot
from telebot.types import Message

from apps.ticket.models import BotUsers


def set_language(bot: TeleBot, message: Message):
    user_id = message.from_user.id
    language_code = message.from_user.language_code[:2]
    language_code = (
        language_code if language_code in dict(BotUsers.LANGUAGE_CODE).keys() else "uz"
    )
    activate(language_code)
    bot.temp_data = {user_id: language_code}
