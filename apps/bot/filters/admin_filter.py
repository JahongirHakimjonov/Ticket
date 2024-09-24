from telebot.custom_filters import SimpleCustomFilter

from apps.ticket.models import BotUsers


class AdminFilter(SimpleCustomFilter):
    """
    Filter for admin users
    """

    key = "admin"

    def check(self, message):
        admins = BotUsers.objects.exclude(role="user").values_list(
            "telegram_id", flat=True
        )
        return message.from_user.id in admins
