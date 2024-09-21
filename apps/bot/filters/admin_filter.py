from telebot.custom_filters import SimpleCustomFilter


class AdminFilter(SimpleCustomFilter):
    """
    Filter for admin users
    """

    key = "admin"

    def check(self, message):
        return message.from_user.id in [483578239, 987654321]  # Add your admin ids here
