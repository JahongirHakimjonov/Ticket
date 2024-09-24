from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_buttons():
    buttons = [
        [KeyboardButton("Concert")],
        [KeyboardButton("Donate")],
        [KeyboardButton("My Bilets")],
        [KeyboardButton("Info")],
        [KeyboardButton("Language")],
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[button for row in buttons for button in row])
    return markup
