import os

from django.utils.translation import activate, gettext as _
from telebot import TeleBot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    WebAppInfo,
)

from apps.bot.logger import logger
from apps.bot.utils.language import set_language_code
from apps.ticket.models import Concert, SeatType, Seat


def handle_buy_ticket_callback(call: CallbackQuery, bot: TeleBot):
    try:
        activate(set_language_code(call.from_user.id))
        concert_id = int(call.data.split("_")[2])
        logger.info(f"Concert ID: {concert_id}")

        # Get the seat types associated with the concert
        seat_type_ids = (
            Seat.objects.filter(concert_id=concert_id, is_active=True, count__gt=0)
            .values_list("type", flat=True)
            .distinct()
        )
        seats_types = SeatType.objects.filter(
            id__in=seat_type_ids, is_active=True
        ).order_by("created_at")
        concert = Concert.objects.get(id=concert_id)
        logger.info(f"Seats found: {seats_types.count()}")

        if seats_types.exists():
            inline_markup = InlineKeyboardMarkup()
            inline_markup.add(
                InlineKeyboardButton(
                    _("Joylashuvni tanlang"), callback_data="choice_type"
                ),
            )
            if concert.map:
                web_app = WebAppInfo(f"{os.getenv('BASE_URL')}{concert.map.url}")
                inline_markup.add(
                    InlineKeyboardButton(_("Sahna chizmasi"), web_app=web_app),
                )
            for seat_type in seats_types:
                inline_markup.add(
                    InlineKeyboardButton(
                        _(f"{seat_type.name}"),
                        callback_data=f"select_seat_{seat_type.id}_{concert_id}",
                    )
                )

            bot.edit_message_reply_markup(
                call.message.chat.id,
                call.message.message_id,
                reply_markup=inline_markup,
            )
        else:
            activate(set_language_code(call.from_user.id))
            bot.answer_callback_query(
                call.id, _("No seats available for this concert.")
            )
    except Exception as e:
        bot.answer_callback_query(call.id, _("An error occurred."))
        logger.error(f"Error while handling buy ticket callback: {e}")
