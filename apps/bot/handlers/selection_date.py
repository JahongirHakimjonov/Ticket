from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import Message

from apps.bot.logger import logger
from apps.bot.utils.language import set_language_code
from apps.ticket.models import Concert
from django.utils.translation import activate, gettext as _


def handle_date_selection(message: Message, bot: TeleBot):
    try:
        activate(set_language_code(message.from_user.id))
        if message.text == _("All"):
            concerts = Concert.objects.filter(is_active=True)
            logger.info(f"Concerts found: {concerts.count()}")
            if concerts.exists():
                for concert in concerts:
                    bot.send_photo(
                        message.chat.id,
                        photo=concert.photo,
                        caption=_(
                            f"{concert.name}\n\n{concert.title}\n\n"
                            f"Sana \ Дата: {concert.date.strftime('%d.%m.%Y')}\nVaqti \ Время: {concert.time.strftime('%H:%M')}\n\n"
                            f"{concert.description}\n\n"
                            f"*📍Manzil \ Адрес:* {concert.address}\n\n"
                            f"[📍Google Xarita \ Карта Google]({concert.location_google_maps})\n[📍Yandex Xarita \ Яндекс Карта]({concert.location_yandex_maps})\n\n"
                            f"*💸Narxlar \ Цены:* {concert.min_price:,} UZS - {concert.max_price:,} UZS\n"
                        ),
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup().add(
                            InlineKeyboardButton(
                                _("Buy Tickets"),
                                callback_data=f"buy_ticket_{concert.id}",
                            )
                        ),
                    )
            else:
                bot.send_message(
                    message.chat.id, _("No active concerts found for this date.")
                )
        else:
            selected_date = message.text
            concerts = Concert.objects.filter(date=selected_date, is_active=True)
            logger.info(f"Concerts found: {concerts.count()}")
            if concerts.exists():
                for concert in concerts:
                    bot.send_photo(
                        message.chat.id,
                        photo=concert.photo,
                        caption=_(
                            f"{concert.name}\n\n{concert.title}\n\n"
                            f"Sana \ Дата: {concert.date.strftime('%d.%m.%Y')}\nVaqti \ Время: {concert.time.strftime('%H:%M')}\n\n"
                            f"{concert.description}\n\n"
                            f"*📍Manzil \ Адрес:* {concert.address}\n\n"
                            f"[📍Google Xarita \ Карта Google]({concert.location_google_maps})\n[📍Yandex Xarita \ Яндекс Карта]({concert.location_yandex_maps})\n\n"
                            f"*💸Narxlar \ Цены:* {concert.min_price:,} UZS - {concert.max_price:,} UZS\n"
                        ),
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup().add(
                            InlineKeyboardButton(
                                _("Buy Tickets"),
                                callback_data=f"buy_ticket_{concert.id}",
                            )
                        ),
                    )
            else:
                bot.send_message(
                    message.chat.id, _("No active concerts found for this date.")
                )
    except Exception as e:
        bot.send_message(message.chat.id, _("An error occurred."))
        logger.error(f"Error while handling date selection: {e}")
