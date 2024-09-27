from django.utils.translation import activate, gettext as _
from telebot import TeleBot
from telebot.types import Message

from apps.bot.utils.language import set_language_code
from apps.ticket.models import Info


def handle_info(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    infos = Info.objects.filter(is_active=True)
    if not infos.exists():
        bot.send_message(message.chat.id, text=_("Hozircha ma'lumotlar mavjud emas"))
        return

    for info in infos:
        text = (
            f"{info.name}\n\n{info.description}\n\n*☎️Telefon \ Телефон:* {info.phone}\n\n"
            f"[📱Telegram:]({info.username})\n\n*📧Email:* {info.email}\n\n"
            f"*🌏Manzil \ Адрес:* {info.address}\n[📍Xarita \ Карта]({info.location})"
        )
        bot.send_message(
            message.chat.id,
            text=text,
            disable_web_page_preview=True,
            parse_mode="Markdown",
        )
