from telebot import TeleBot
from telebot.types import Message

from apps.ticket.models import Info


def handle_info(message: Message, bot: TeleBot):
    infos = Info.objects.filter(is_active=True)
    if not infos.exists():
        bot.send_message(message.chat.id, text="Hozircha ma'lumotlar mavjud emas")
        return

    for info in infos:
        text = (
            f"{info.name}\n\n{info.description}\n\n*☎️Telefon raqam:* {info.phone}\n"
            f"*📱Telegram:* {info.username}\n*📧Email:* {info.email}\n\n"
            f"*🌏Manzil:* {info.address}\n[📍Xaritada ko'rish]({info.location})"
        )
        bot.send_message(
            message.chat.id,
            text=text,
            disable_web_page_preview=True,
            parse_mode="Markdown",
        )
