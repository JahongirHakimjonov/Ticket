from django.utils.translation import activate, gettext as _
from telebot import TeleBot
from telebot.types import Message

from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import set_language_code
from apps.ticket.models import Info


def handle_info(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    update_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        is_active=True,
    )
    infos = Info.objects.filter(is_active=True)
    if not infos.exists():
        bot.send_message(message.chat.id, text=_("Hozircha ma'lumotlar mavjud emas"))
        return

    for info in infos:
        text = f"{info.name}\n\n{info.description}\n" f"{info.username}"
        bot.send_message(
            message.chat.id,
            text=text,
        )
