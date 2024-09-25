from telebot import TeleBot, types
from telebot.types import Message, CallbackQuery

from apps.ticket.models import BotUsers, Donate


def handle_donate(message: Message, bot: TeleBot):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    # Create buttons for numbers from 10,000 to 100,000
    buttons = [
        types.InlineKeyboardButton(text=str(i), callback_data=str(i))
        for i in range(10000, 100001, 10000)
    ]

    keyboard.add(*buttons)

    # Add a cancel button
    cancel_button = types.InlineKeyboardButton(text="Cancel", callback_data="cancel")
    keyboard.add(cancel_button)

    bot.send_message(
        message.chat.id, "Select an amount to donate:", reply_markup=keyboard
    )


def handle_cancel(call: CallbackQuery, bot: TeleBot):
    bot.delete_message(call.message.chat.id, call.message.message_id)


def handle_donation(call: CallbackQuery, bot: TeleBot):
    amount = int(call.data)
    user = BotUsers.objects.get(
        telegram_id=call.from_user.id
    )  # Assuming you have a way to get the user
    Donate.objects.create(user=user, amount=amount)
    inline = types.InlineKeyboardMarkup()
    inline.add(types.InlineKeyboardButton(text="PAYME", url="https://payme.uz"))
    bot.send_message(
        call.message.chat.id,
        f"Siz bizga {amount} so'm mablag'ni jo'natdingiz. Rahmat!\nTugmani bosing⬇️",
        reply_markup=inline,
    )
    bot.delete_message(call.message.chat.id, call.message.message_id)
