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
    concert_dates = (
        Concert.objects.filter(is_active=True).values_list("date", flat=True).distinct()
    )
    all_concerts = Concert.objects.filter(is_active=True)

    if len(all_concerts) == 1:
        # If there is only one concert, get the single instance
        concert_details = all_concerts.first()
        bot.send_photo(
            message.chat.id,
            photo=concert_details.photo,
            caption=f"{concert_details.name}\n\n{concert_details.title}\n\n"
            f"Sana: {concert_details.date.strftime('%d.%m.%Y')}\nVaqti: {concert_details.time.strftime('%H:%M')}\n\n"
            f"{concert_details.description}\n\n"
            f"*📍Manzil:* {concert_details.address}\n\n"
            f"[📍Google Xarita]({concert_details.location_google_maps})\n[📍Yandex Xarita]({concert_details.location_yandex_maps})\n\n"
            f"*💸Narxlar:* {concert_details.min_price:,} UZS - {concert_details.max_price:,} UZS\n",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    "Buy Tickets", callback_data=f"buy_ticket_{concert_details.id}"
                )
            ),
        )
    else:
        # Inline button
        inline_markup = InlineKeyboardMarkup()
        inline_button = InlineKeyboardButton(
            "Search Concerts", switch_inline_query_current_chat=""
        )

        keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for date in concert_dates:
            keyboard_button = KeyboardButton(str(date))
            keyboard_markup.add(keyboard_button)

        all_button = KeyboardButton("All")
        home_button = KeyboardButton("Home")
        keyboard_markup.add(all_button)
        keyboard_markup.add(home_button)
        inline_markup.add(inline_button)

        bot.send_message(
            message.chat.id,
            "Please select a concert date or search for concerts:",
            reply_markup=inline_markup,
        )
        bot.send_message(
            message.chat.id, "Available concert dates:", reply_markup=keyboard_markup
        )
