from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import activate, gettext as _


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
