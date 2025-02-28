from django.utils import timezone
from django.utils.translation import activate, gettext as _
from telebot import TeleBot
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    Message,
)

from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import set_language_code
from apps.ticket.models import Concert  # Import the Concert model


def handle_concert(message: Message, bot: TeleBot):
    concert_dates = (
        Concert.objects.filter(is_active=True)
        .values_list("date", flat=True)
        .distinct()
        .first()
    )
    activate(set_language_code(message.from_user.id))
    update_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        is_active=True,
    )
    all_concerts = Concert.objects.filter(is_active=True, date__gte=timezone.now())
    if all_concerts.exists():
        if len(all_concerts) == 1:
            # If there is only one concert, get the single instance
            concert_details = all_concerts.first()
            bot.send_photo(
                message.chat.id,
                photo=concert_details.photo,
                caption=_(
                    f"{concert_details.name}\n\n{concert_details.title}\n\n"
                    f"Sana \ Дата: {concert_details.date.strftime('%d.%m.%Y')}\nVaqti \ Время: {concert_details.time.strftime('%H:%M')}\n\n"
                    f"{concert_details.description}\n\n"
                    f"*📍Manzil \ Адрес:* {concert_details.address}\n\n"
                    f"[📍Google Xarita \ Карта Google]({concert_details.location_google_maps})\n[📍Yandex Xarita \ Яндекс Карта]({concert_details.location_yandex_maps})\n\n"
                    f"*💸Narxlar \ Цены:* {concert_details.min_price:,} UZS - {concert_details.max_price:,} UZS\n"
                ),
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        _("Buy Tickets"),
                        callback_data=f"buy_ticket_{concert_details.id}",
                    )
                ),
            )
        else:
            # Inline button
            inline_markup = InlineKeyboardMarkup()
            inline_button = InlineKeyboardButton(
                _("Search Concerts"), switch_inline_query_current_chat=""
            )

            keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)

            # Add the "All" button first
            all_button = KeyboardButton(_("All"))
            keyboard_markup.add(all_button)

            # Add the date buttons next
            keyboard_button = KeyboardButton(str(concert_dates))
            keyboard_markup.add(keyboard_button)

            # Add the "Home" button last
            home_button = KeyboardButton(_("Home"))
            keyboard_markup.add(home_button)

            # Add the inline button
            inline_markup.add(inline_button)

            bot.send_message(
                message.chat.id,
                _("Please select a concert date or search for concerts:"),
                reply_markup=inline_markup,
            )
            bot.send_message(
                message.chat.id,
                _("Available concert dates:"),
                reply_markup=keyboard_markup,
            )
    else:
        bot.send_message(message.chat.id, _("No active concerts available."))
