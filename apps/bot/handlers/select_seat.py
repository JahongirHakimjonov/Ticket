from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from apps.bot.logger import logger
from apps.bot.utils.language import set_language_code
from apps.ticket.models import Seat
from django.utils.translation import activate, gettext as _


def handle_select_seat_callback(call: CallbackQuery, bot: TeleBot):
    try:
        activate(set_language_code(call.from_user.id))
        seat_id = int(call.data.split("_")[2])
        seat = Seat.objects.get(id=seat_id)
        logger.info(f"Seat selected: {seat.name}")

        inline_markup = InlineKeyboardMarkup()
        buttons = []

        # Add "Select Quantity" button at the top
        inline_markup.add(
            InlineKeyboardButton(_("Select Quantity"), callback_data="noop")
        )

        if seat.count > 50:
            max_buttons = 50
        else:
            max_buttons = seat.count

        for i in range(1, max_buttons + 1):
            buttons.append(
                InlineKeyboardButton(
                    str(i), callback_data=f"select_count_{seat_id}_{i}"
                )
            )

        # Add buttons in rows of 5
        for i in range(0, len(buttons), 5):
            inline_markup.row(*buttons[i : i + 5])

        # Add "Back" button at the bottom
        inline_markup.add(
            InlineKeyboardButton(
                _("Back"), callback_data=f"buy_ticket_{seat.concert.id}"
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
