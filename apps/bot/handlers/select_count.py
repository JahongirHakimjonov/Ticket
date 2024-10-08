import os

from django.db.models import Sum
from django.utils.translation import activate, gettext as _
from telebot import TeleBot
from telebot.types import CallbackQuery
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from apps.bot.logger import logger
from apps.bot.utils.language import set_language_code
from apps.ticket.models import BotUsers, Order, Seat, SeatNumber

selected_set_numbers = {}


def handle_select_count_callback(call: CallbackQuery, bot: TeleBot):
    try:
        activate(set_language_code(call.from_user.id))
        user_id = call.from_user.id
        seat_id = int(call.data.split("_")[2])
        logger.info(f"Seat ID: {seat_id}")

        # Initialize the user's selected set numbers if not already done
        if user_id not in selected_set_numbers:
            selected_set_numbers[user_id] = set()

        # Retrieve the seat object
        try:
            seat = Seat.objects.get(id=seat_id)
        except Seat.DoesNotExist:
            bot.answer_callback_query(call.id, _("Seat does not exist."))
            logger.error(f"Seat with ID {seat_id} does not exist.")
            return

        logger.info(f"User id: {user_id}")

        # Retrieve the user object
        user = BotUsers.objects.get(telegram_id=user_id)

        # Check the total number of tickets already purchased for the concert
        total_tickets = (
            Order.objects.filter(
                user=user, concert=seat.concert, is_paid=True
            ).aggregate(total=Sum("count"))["total"]
            or 0
        )
        logger.info(f"Total tickets: {total_tickets}")

        # Create new inline keyboard
        inline_markup = InlineKeyboardMarkup(row_width=5)
        inline_markup.add(
            InlineKeyboardButton(_("O'rindiqni tanlang"), callback_data="seat"),
        )
        # Add "Sahna chizmasi" button at the top
        if seat.concert and seat.concert.map:
            web_app = WebAppInfo(f"{os.getenv('BASE_URL')}{seat.concert.map.url}")
            inline_markup.add(
                InlineKeyboardButton(_("Sahna chizmasi"), web_app=web_app),
            )

        # Retrieve all SetNumber objects related to the seat
        set_numbers = SeatNumber.objects.filter(seat=seat, is_active=True).order_by(
            "id"
        )

        buttons = [
            InlineKeyboardButton(
                _(
                    f"{set_number.number} {'✅' if set_number.id in selected_set_numbers[user_id] else ''}"
                ),
                callback_data=f"select_setnumber_{set_number.id}_{seat_id}",
            )
            for set_number in set_numbers
        ]
        inline_markup.add(*buttons)

        # Confirm button at the bottom
        inline_markup.add(
            InlineKeyboardButton(_("Tasdiqlash"), callback_data=f"confirm_{seat.id}")
        )

        # Add "Back" button at the bottom
        inline_markup.add(
            InlineKeyboardButton(
                _("Back"), callback_data=f"select_seat_{seat.type.id}_{seat.concert.id}"
            )
        )

        # Update the message with the new inline keyboard
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=inline_markup,
        )

        bot.answer_callback_query(call.id, _("Set numbers loaded."))
    except Exception as e:
        bot.answer_callback_query(call.id, _("An error occurred."))
        logger.error(f"Error while handling select count callback: {e}")


def handle_setnumber_selection(call: CallbackQuery, bot: TeleBot):
    try:
        logger.info(f"====================")
        logger.info(f"Callback Data: {call.data}")
        logger.info(f"====================")
        activate(set_language_code(call.from_user.id))
        user_id = call.from_user.id
        data_parts = call.data.split("_")
        if (
            len(data_parts) < 4
            or not data_parts[2].isdigit()
            or not data_parts[3].isdigit()
        ):
            raise ValueError("Callback data format is incorrect")

        set_number_id = int(data_parts[2])  # set_number.id bo'lishi kerak
        seat_id = int(data_parts[3])  # seat_id bo'lishi kerak

        if user_id not in selected_set_numbers:
            selected_set_numbers[user_id] = set()

        if set_number_id in selected_set_numbers[user_id]:
            selected_set_numbers[user_id].remove(set_number_id)
        else:
            selected_set_numbers[user_id].add(set_number_id)

        # Refresh the buttons in real-time
        seat = Seat.objects.get(id=seat_id)
        set_numbers = SeatNumber.objects.filter(seat=seat, is_active=True).order_by(
            "id"
        )

        inline_markup = InlineKeyboardMarkup(row_width=5)
        inline_markup.add(
            InlineKeyboardButton(_("O'rindiqni tanlang"), callback_data="seat"),
        )
        # Add "Sahna chizmasi" button at the top
        if seat.concert and seat.concert.map:
            web_app = WebAppInfo(f"{os.getenv('BASE_URL')}{seat.concert.map.url}")
            inline_markup.add(
                InlineKeyboardButton(_("Sahna chizmasi"), web_app=web_app),
            )

        buttons = [
            InlineKeyboardButton(
                _(
                    f"{set_number.number} {'✅' if set_number.id in selected_set_numbers[user_id] else ''}"
                ),
                callback_data=f"select_setnumber_{set_number.id}_{seat_id}",
            )
            for set_number in set_numbers
        ]
        inline_markup.add(*buttons)

        # Confirm button at the bottom
        inline_markup.add(
            InlineKeyboardButton(_("Tasdiqlash"), callback_data=f"confirm_{seat.id}")
        )

        # Add "Back" button at the bottom
        inline_markup.add(
            InlineKeyboardButton(
                _("Back"), callback_data=f"select_seat_{seat.type.id}_{seat.concert.id}"
            )
        )

        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=inline_markup,
        )

        bot.answer_callback_query(call.id, _("Set number selection updated."))
    except Exception as e:
        bot.answer_callback_query(call.id, _("An error occurred."))
        logger.error(f"Error while handling set number selection: {e}")


def handle_confirm_selection(call: CallbackQuery, bot: TeleBot):
    try:
        user_id = call.from_user.id
        user = BotUsers.objects.get(telegram_id=user_id)
        activate(set_language_code(user_id))
        seat_id = int(call.data.split("_")[1])
        logger.info(f"Confirming selection for Seat ID: {seat_id}")
        seat = Seat.objects.get(id=seat_id)
        order = Order.objects.create(
            user=user,
            concert=seat.concert,
            seat=seat,
        )
        order.seat_numbers.set(selected_set_numbers.get(user_id, set()))
        order.save()
        inline_markup = InlineKeyboardMarkup()
        inline_markup.add(
            InlineKeyboardButton(_("Select Payment"), callback_data="select_payment")
        )
        inline_markup.add(
            InlineKeyboardButton("PAYME", callback_data=f"payme_{order.id}")
        )

        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=inline_markup,
        )

        bot.answer_callback_query(call.id, _("Order created successfully."))

        # Clear the selected set numbers for the user
        selected_set_numbers.pop(user_id, None)

    except Exception as e:
        bot.answer_callback_query(call.id, _("An error occurred."))
        logger.error(f"Error while confirming selection: {e}")
