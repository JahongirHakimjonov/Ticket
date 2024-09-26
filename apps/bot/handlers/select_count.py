from telebot import TeleBot
from telebot.types import CallbackQuery
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from apps.bot.logger import logger
from apps.ticket.models import BotUsers
from apps.ticket.models import Order, Seat


def handle_select_count_callback(call: CallbackQuery, bot: TeleBot):
    try:
        data = call.data.split("_")
        seat_id = int(data[2])
        count = int(data[3])
        logger.info(f"Seat ID: {seat_id}, Count: {count}")

        # Retrieve the seat object
        seat = Seat.objects.get(id=seat_id)
        logger.info(f"User id: {call.from_user.id}")

        # Retrieve the user object
        user = BotUsers.objects.get(telegram_id=call.from_user.id)

        # Create the Order object
        order = Order.objects.create(
            seat=seat, count=count, user=user, concert=seat.concert
        )
        logger.info(f"Order created: {order.id}")

        # Create new inline keyboard with "Select Payment" and "PayMe" buttons
        inline_markup = InlineKeyboardMarkup()
        inline_markup.add(
            InlineKeyboardButton("Select Payment", callback_data="select_payment")
        )
        inline_markup.add(InlineKeyboardButton("PayMe", callback_data=f"payme_{order.id}"))

        # Update the message with the new inline keyboard
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=inline_markup,
        )

        bot.answer_callback_query(call.id, f"{count} tickets selected.")
    except Exception as e:
        bot.answer_callback_query(call.id, "An error occurred.")
        logger.error(f"Error while handling select count callback: {e}")
