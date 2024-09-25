from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from apps.bot.logger import logger
from apps.ticket.models import Seat


def handle_buy_ticket_callback(call: CallbackQuery, bot: TeleBot):
    try:
        concert_id = int(call.data.split("_")[2])
        logger.info(f"Concert ID: {concert_id}")
        seats = Seat.objects.filter(concert_id=concert_id, is_active=True, count__gt=0)
        logger.info(f"Seats found: {seats.count()}")

        if seats.exists():
            inline_markup = InlineKeyboardMarkup()
            for seat in seats:
                inline_markup.add(
                    InlineKeyboardButton(
                        f"{seat.name} - {seat.price:,} UZS, Mavjud: {seat.count}",
                        callback_data=f"select_seat_{seat.id}",
                    )
                )

            bot.edit_message_reply_markup(
                call.message.chat.id,
                call.message.message_id,
                reply_markup=inline_markup,
            )
        else:
            bot.answer_callback_query(call.id, "No seats available for this concert.")
    except Exception as e:
        bot.answer_callback_query(call.id, "An error occurred.")
        logger.error(f"Error while handling buy ticket callback: {e}")
