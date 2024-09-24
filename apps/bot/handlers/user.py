from telebot import TeleBot
from telebot.types import Message

from apps.ticket.models import Concert


def any_user(message: Message, bot: TeleBot):
    try:
        if message.text.startswith('/start '):
            concert_id = message.text.split(' ')[1]
            concert = Concert.objects.get(id=concert_id)
            if concert.is_active:
                thumbnail_url = (
                    "https://classcom.felixits.uz/media/documents/2024/09/23/2_1.jpg"
                )
                bot.send_photo(
                    message.chat.id,
                    photo=concert.photo,
                    caption=f"{concert.name}\n\n{concert.title}\n\n"
                    f"Sana: {concert.date.strftime('%d.%m.%Y')}\nVaqti: {concert.time.strftime('%H:%M')}\n\n"
                    f"{concert.description}\n\n[ ]({thumbnail_url})\n"
                    f"*📍Manzil:* {concert.address}\n\n"
                    f"[📍Google Xarita]({concert.location_google_maps})\n[📍Yandex Xarita]({concert.location_yandex_maps})\n\n"
                    f"*💸Narxlar:* {concert.min_price:,} UZS - {concert.max_price:,} UZS\n",
                    parse_mode="Markdown"
                )
            else:
                bot.send_message(message.chat.id, "This concert is not active.")
        else:
            bot.send_message(message.chat.id, "Welcome to the bot! Use the inline buttons to search for concerts.")
    except Concert.DoesNotExist:
        bot.send_message(message.chat.id, "Concert not found.")
    except Exception as e:
        bot.send_message(message.chat.id, "An error occurred.")
        print(e)
