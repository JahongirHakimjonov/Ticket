from shortuuid import uuid
from telebot import TeleBot, types
from telebot.types import Message, CallbackQuery

from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import set_language_code
from apps.bot.utils.link import GeneratePayLink
from apps.payme.utils.logging import logger
from apps.payment.models import Payment
from apps.ticket.models import BotUsers, Donate
from django.utils.translation import activate, gettext_lazy as _


def handle_donate(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    update_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        is_active=True,
    )
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    # Create buttons for numbers from 10,000 to 100,000
    buttons = [
        types.InlineKeyboardButton(text=str(f"{i:,}"), callback_data=str(i))
        for i in [100000, 200000, 300000, 400000, 500000, 1000000, 10000000]
    ]

    keyboard.add(*buttons)

    # Add a cancel button
    cancel_button = types.InlineKeyboardButton(
        text=str(_("Cancel")), callback_data="cancel"
    )
    keyboard.add(cancel_button)

    bot.send_message(
        message.chat.id, str(_("Select an amount to donate:")), reply_markup=keyboard
    )


def handle_cancel(call: CallbackQuery, bot: TeleBot):
    activate(set_language_code(call.from_user.id))
    bot.delete_message(call.message.chat.id, call.message.message_id)


def handle_donation(call: CallbackQuery, bot: TeleBot):
    activate(set_language_code(call.from_user.id))
    amount = int(call.data)
    user = BotUsers.objects.get(
        telegram_id=call.from_user.id
    )  # Assuming you have a way to get the user
    donate = Donate.objects.create(user=user, amount=amount)
    order_id = f"donate_{uuid()}_{donate.id}"
    payment = Payment.objects.create(
        order_id=order_id,
        status="PROCESSING",
        type="DONATE",
        amount=donate.amount * 100,
        transaction_id=donate.id,
    )
    pay_link = GeneratePayLink(
        order_id=order_id,
        amount=GeneratePayLink.to_tiyin(donate.amount),
    ).generate_link()
    inline = types.InlineKeyboardMarkup()
    inline.add(types.InlineKeyboardButton(text="PAYME", url=pay_link))
    if set_language_code(call.from_user.id) == "uz":
        bot.send_message(
            call.message.chat.id,
            text=str(
                f"Siz bizga {amount} so'm mablag'ni jo'natdingiz. Rahmat!\nTugmani bosing va to'lovni amalga oshiring."
            ),
            reply_markup=inline,
        )
    else:
        bot.send_message(
            call.message.chat.id,
            text=str(
                f"Вы пожертвовали {amount} UZS. Спасибо!\nНажмите кнопку и продолжите оплату."
            ),
            reply_markup=inline,
        )
    bot.delete_message(call.message.chat.id, call.message.message_id)
