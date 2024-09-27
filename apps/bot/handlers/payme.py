from shortuuid import uuid
from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from apps.bot.logger import logger
from apps.bot.utils.language import set_language_code
from apps.bot.utils.link import GeneratePayLink
from apps.payment.models import Payment
from apps.ticket.models import Info, Order
from django.utils.translation import activate, gettext as _

# Initialize the bot with state storage
state_storage = StateMemoryStorage()


def handle_payme_callback(call: CallbackQuery, bot: TeleBot):
    try:
        activate(set_language_code(call.from_user.id))
        # Create new inline keyboard with "Select Payment" and "✅PayMe" buttons
        order = Order.objects.get(id=call.data.split("_")[1])
        order_id = f"order_{uuid()}_{order.id}"
        payment = Payment.objects.create(
            order_id=order_id,
            status="PROCESSING",
            type="ORDER",
            amount=order.total_price,
            transaction_id=order.id,
        )
        inline_markup = InlineKeyboardMarkup()
        inline = InlineKeyboardMarkup()
        inline_markup.add(
            InlineKeyboardButton(_("Select Payment"), callback_data="select_payment")
        )
        inline_markup.add(
            InlineKeyboardButton("✅Payme", callback_data="payme_checked")
        )
        pay_link = GeneratePayLink(
            order_id=order_id,
            amount=GeneratePayLink.to_sum(payment.amount * 100),
        ).generate_link()
        inline.add(InlineKeyboardButton(_("Select Payment"), url=pay_link))

        # Update the message with the new inline keyboard
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=inline_markup,
        )
        info = Info.objects.all().last()
        if set_language_code(call.from_user.id) == "uz":
            bot.send_message(
                call.message.chat.id,
                _(
                    f"Sizning buyurtmangiz qabul qilindi,\bBuyurtmaning umumiy summasi {order.total_price:,} iltimos, to'lovni amalga oshiring.\nOperator bilan bog'lanish uchun 👉 {info.username}\nTelefon: {info.phone}"
                ),
            )
        else:
            bot.send_message(
                call.message.chat.id,
                _(
                    f"Ваш заказ принят,\bОбщая сумма заказа составляет {order.total_price:,}, пожалуйста, произведите оплату.\nДля связи с оператором 👉 {info.username}\nТелефон: {info.phone}"
                ),
            )
        bot.send_message(
            call.message.chat.id, _("Payme selected."), reply_markup=inline
        )

        # Set the state to Order.full_name
        # bot.set_state(call.from_user.id, Order.full_name, call.message.chat.id)
        # bot.send_message(call.message.chat.id, "Iltimos, to'liq ismingizni kiriting:")

        bot.answer_callback_query(call.id, _("Payme selected."))
    except Exception as e:
        bot.answer_callback_query(call.id, _("An error occurred."))
        logger.error(f"Error while handling PayMe callback: {e}")
