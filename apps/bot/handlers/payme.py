import re

from django.utils.translation import activate, gettext as _
from shortuuid import uuid
from telebot import TeleBot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

user_states = {}

AWAITING_FULL_NAME = "awaiting_full_name"
AWAITING_PHONE_NUMBER = "awaiting_phone_number"

from apps.bot.keyboard import get_main_buttons
from apps.bot.logger import logger
from apps.bot.utils.language import set_language_code
from apps.bot.utils.link import GeneratePayLink
from apps.payment.models import Payment
from apps.ticket.models import Info, Order

from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def handle_payme_callback(call: CallbackQuery, bot: TeleBot):
    try:
        activate(set_language_code(call.from_user.id))

        # Orderni olish
        order = Order.objects.get(id=call.data.split("_")[1])

        # To'lov tugmasi bilan klaviatura yaratish
        inline_markup = InlineKeyboardMarkup()
        inline_markup.add(
            InlineKeyboardButton(_("Select Payment"), callback_data="select_payment")
        )
        inline_markup.add(
            InlineKeyboardButton("✅Payme", callback_data="payme_checked")
        )

        # Xabarni yangilash
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=inline_markup,
        )

        # Foydalanuvchidan telefon raqami so'rash
        request_phone_keyboard = ReplyKeyboardMarkup(
            one_time_keyboard=True, resize_keyboard=True
        )
        request_phone_keyboard.add(
            KeyboardButton(text=_("📞 Telefon raqamni yuboring"), request_contact=True)
        )

        bot.send_message(
            call.message.chat.id,
            _("Iltimos, telefon raqamingizni yuboring yoki yozing:"),
            reply_markup=request_phone_keyboard,
        )

        # Telefon raqamni qabul qilgandan keyin ism/familiyani so'rashga o'tish
        bot.register_next_step_handler(call.message, process_phone_number, bot, order)

    except Exception as e:
        bot.answer_callback_query(call.id, _("Xatolik yuz berdi."))
        logger.error(f"PayMe callbackni qayta ishlashda xatolik: {e}")


# Telefon raqamini qayta ishlash
def process_phone_number(message, bot: TeleBot, order):
    try:
        if message.contact:
            # User sent phone number as contact
            phone_number = message.contact.phone_number
        else:
            regex_pattern = r"^\+?998[\d\s\-\(\)]{9,13}$"
            # User sent phone number as text
            phone_number = (
                message.text if re.match(regex_pattern, message.text) else None
            )

        if phone_number:
            # Save phone number to order
            order.user.phone = phone_number
            order.phone = phone_number
            order.user.save()
            order.save()

            # Ask for full name
            bot.send_message(
                message.chat.id, _("Iltimos, to'liq ismingizni yozing (Ism Familiya):")
            )

            # Proceed to process full name
            bot.register_next_step_handler(message, process_full_name, bot, order)
        else:
            # Ask for phone number again
            bot.send_message(
                message.chat.id, _("Noto'g'ri telefon raqami. Iltimos, qayta kiriting:")
            )
            bot.register_next_step_handler(message, process_phone_number, bot, order)

    except Exception as e:
        bot.send_message(message.chat.id, _("Xatolik yuz berdi."))
        logger.error(f"Telefon raqamini qayta ishlashda xatolik: {e}")


# To'liq ismni qayta ishlash
def process_full_name(message, bot: TeleBot, order):
    try:
        # Foydalanuvchining ism/familiyasini qabul qilish
        full_name = message.text

        # Ismni orderga saqlash
        order.user.full_name = full_name
        order.full_name = full_name
        order.user.save()
        order.save()

        # To'lov haqida ma'lumot yuborish
        info = Info.objects.all().last()
        if info.username is None:
            info.username = "???"
        if info.phone is None:
            info.phone = "???"
        if set_language_code(message.from_user.id) == "uz":
            bot.send_message(
                message.chat.id,
                _(
                    f"Sizning buyurtmangiz qabul qilindi,\nBuyurtmaning umumiy summasi {order.total_price:,} so'm.\n"
                    f"Operator bilan bog'lanish uchun 👉 {info.username}\nTelefon: {info.phone}"
                ),
                reply_markup=get_main_buttons(),
            )
        else:
            bot.send_message(
                message.chat.id,
                _(
                    f"Ваш заказ принят,\nОбщая сумма заказа {order.total_price:,} сум.\n"
                    f"Для связи с оператором 👉 {info.username}\nТелефон: {info.phone}"
                ),
                reply_markup=get_main_buttons(),
            )

        order_id = f"order_{uuid()}_{order.id}"

        # Paymentni yaratish
        Payment.objects.create(
            order_id=order_id,
            status="PROCESSING",
            type="ORDER",
            amount=order.total_price,
            transaction_id=order.id,
        )

        # Yana Payme linkini yuborish
        bot.send_message(
            message.chat.id,
            _("Payme tanlandi."),
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    _("To'lovni amalga oshiring"),
                    url=GeneratePayLink(
                        order_id=order_id,
                        amount=GeneratePayLink.to_tiyin(order.total_price),
                    ).generate_link(),
                )
            ),
        )

    except Exception as e:
        bot.send_message(message.chat.id, _("Xatolik yuz berdi."))
        logger.error(f"Ismni qayta ishlashda xatolik: {e}")
