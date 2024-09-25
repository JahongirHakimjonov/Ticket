from telebot import TeleBot, types
from telebot.types import Message


def handle_ticket(message: Message, bot: TeleBot):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_active_tickets = types.KeyboardButton("Active Tickets")
    btn_all_tickets = types.KeyboardButton("All Tickets")
    btn_back = types.KeyboardButton("Home")
    keyboard.add(btn_active_tickets, btn_all_tickets, btn_back)

    bot.send_message(
        message.chat.id, "Kerakli bo'limni tanlang:", reply_markup=keyboard
    )
