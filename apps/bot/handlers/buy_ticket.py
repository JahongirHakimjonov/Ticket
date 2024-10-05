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
from apps.ticket.models import Seat, Concert


def handle_buy_ticket_callback(call: CallbackQuery, bot: TeleBot):
    try:
        activate(set_language_code(call.from_user.id))
        concert_id = int(call.data.split("_")[2])
        logger.info(f"Concert ID: {concert_id}")
        seats = Seat.objects.filter(concert_id=concert_id, is_active=True, count__gt=0)
        concert = Concert.objects.get(id=concert_id)
        logger.info(f"Seats found: {seats.count()}")

        if seats.exists():
            inline_markup = InlineKeyboardMarkup()
            if concert.map:
                web_app = WebAppInfo(f"{os.getenv('BASE_URL')}{concert.map.url}")
                inline_markup.add(
                    InlineKeyboardButton(_("Sahna chizmasi"), web_app=web_app),
                )
            for seat in seats:
                inline_markup.add(
                    InlineKeyboardButton(
                        _(
                            f"{seat.name} - {seat.price:,} UZS, Mavjud \ Есть: {seat.count}"
                        ),
                        callback_data=f"select_seat_{seat.id}",
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
