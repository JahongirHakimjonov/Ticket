from django.utils.translation import gettext as _
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_buttons():
    buttons = [
        [KeyboardButton(_("Concert"))],
        [KeyboardButton(_("Donate"))],
        [KeyboardButton(_("My Tickets"))],
        [KeyboardButton(_("Info"))],
        [KeyboardButton(_("Language"))],
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[button for row in buttons for button in row])
    return markup
