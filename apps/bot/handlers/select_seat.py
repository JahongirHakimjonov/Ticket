import os

from django.utils.translation import activate, gettext as _
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    WebAppInfo,
)

from apps.bot.handlers.select_count import selected_set_numbers
from apps.bot.logger import logger
from apps.bot.utils.language import set_language_code
from apps.ticket.models import Seat


def handle_select_seat_callback(call: CallbackQuery, bot: TeleBot):
    try:
        user_id = call.from_user.id
        selected_set_numbers.pop(user_id, None)
        activate(set_language_code(call.from_user.id))
        seat_type_id = int(call.data.split("_")[2])
        concert_id = int(call.data.split("_")[3])
        seats = Seat.objects.filter(
            type_id=seat_type_id, count__gt=0, concert_id=concert_id, is_active=True
        ).order_by("created_at")
        inline_markup = InlineKeyboardMarkup()

        # Add "Select Quantity" button at the top
        inline_markup.add(
            InlineKeyboardButton(_("Qatorni tanlang"), callback_data="noop")
        )

        if seats.exists():
            concert = seats.first().concert  # Access the concert through the first seat
            if concert and concert.map:
                web_app = WebAppInfo(f"{os.getenv('BASE_URL')}{concert.map.url}")
                inline_markup.add(
                    InlineKeyboardButton(_("Sahna chizmasi"), web_app=web_app),
                )

            for seat in seats:
                inline_markup.add(
                    InlineKeyboardButton(
                        _(f"{seat.name} - {seat.price} UZS"),
                        callback_data=f"select_count_{seat.id}",
                    )
                )

            # Add "Back" button at the bottom
            inline_markup.add(
                InlineKeyboardButton(
                    _("Back"), callback_data=f"buy_ticket_{concert.id}"
                )
            )

        # Check if the new reply markup is different from the current one
        if call.message.reply_markup.to_dict() != inline_markup.to_dict():
            bot.edit_message_reply_markup(
                call.message.chat.id,
                call.message.message_id,
                reply_markup=inline_markup,
            )
        else:
            bot.answer_callback_query(call.id, _("No changes to update."))
    except ApiTelegramException as e:
        if e.result_json["description"] == _(
            "Bad Request: query is too old and response timeout expired or query ID is invalid"
        ):
            bot.answer_callback_query(
                call.id, _("This action took too long. Please try again.")
            )
        else:
            bot.answer_callback_query(call.id, _("An error occurred."))
        logger.error(f"Telegram API error while handling select seat callback: {e}")
    except Exception as e:
        bot.answer_callback_query(call.id, _("An error occurred."))
        logger.error(f"Error while handling select seat callback: {e}")
