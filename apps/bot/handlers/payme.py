from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from apps.bot.handlers.home import handle_message
from apps.bot.logger import logger
from apps.bot.states.order_state import Order
from apps.ticket.models import Info

# Initialize the bot with state storage
state_storage = StateMemoryStorage()


def handle_payme_callback(call: CallbackQuery, bot: TeleBot):
    try:
        # Create new inline keyboard with "Select Payment" and "✅PayMe" buttons
        inline_markup = InlineKeyboardMarkup()
        inline = InlineKeyboardMarkup()
        inline_markup.add(
            InlineKeyboardButton("Select Payment", callback_data="select_payment")
        )
        inline_markup.add(
            InlineKeyboardButton("✅PayMe", callback_data="payme_checked")
        )
        inline.add(InlineKeyboardButton("Select Payment", url="https://payme.uz"))

        # Update the message with the new inline keyboard
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=inline_markup,
        )
        info = Info.objects.all().last()
        bot.send_message(
            call.message.chat.id,
            f"Sizning buyurtmangiz qabul qilindi, iltimos, to'lovni amalga oshiring."
            f"\nOperator bilan bog'lanish uchun 👉 {info.username}\nTelefon: {info.phone}",
        )
        bot.send_message(call.message.chat.id, "PayMe selected.", reply_markup=inline)

        # Set the state to Order.full_name
        bot.set_state(call.from_user.id, Order.full_name, call.message.chat.id)
        bot.send_message(call.message.chat.id, "Iltimos, to'liq ismingizni kiriting:")

        bot.answer_callback_query(call.id, "PayMe selected.")
    except Exception as e:
        bot.answer_callback_query(call.id, "An error occurred.")
        logger.error(f"Error while handling PayMe callback: {e}")


