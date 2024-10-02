import os

from django.utils.translation import activate, gettext as _
from telebot import TeleBot

from apps.bot.utils.language import set_language_code
from apps.payme.utils.logging import logger
from apps.ticket.models import BotUsers, Order, News

bot = TeleBot(os.getenv("BOT_TOKEN"))


def send_telegram_message(order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order and order.is_paid:
            user = order.user
            activate(set_language_code(user.telegram_id))
            logger.info(f"Sending message to {user.telegram_id}")
            if not isinstance(user.telegram_id, int):
                raise ValueError("Invalid telegram_id: must be an integer")
            message = _(
                "To'lov muvaffaqiyatli amalga oshirildi! Biletlarni (Mening biletlarim bo'limidan olishingiz mumkin)\n\n"
            )
            bot.send_message(user.telegram_id, message)
    except BotUsers.DoesNotExist:
        pass
    except ValueError as e:
        logger.error(e)


def send_message(order_id, message):
    try:
        logger.info(f"Sending message to {order_id}")
        order = Order.objects.get(id=order_id)
        user = order.user
        activate(set_language_code(user.telegram_id))
        logger.info(f"Sending message to {user.telegram_id}")
        if not isinstance(user.telegram_id, int):
            raise ValueError("Invalid telegram_id: must be an integer")
        bot.send_message(user.telegram_id, message)
    except BotUsers.DoesNotExist:
        pass
    except ValueError as e:
        logger.error(e)


def send_news(user_id, title, content, image, news_id):
    try:
        user = BotUsers.objects.get(id=user_id)
        news = News.objects.get(id=news_id)
        activate(set_language_code(user.telegram_id))
        logger.info(f"Sending message to {user.telegram_id}")
        if not isinstance(user.telegram_id, int):
            raise ValueError("Invalid telegram_id: must be an integer")
        if not image:
            raise ValueError("Image must be non-empty")
        if (
            image.size > 5 * 1024 * 1024
        ):  # Check if the image size is greater than 10 MB
            raise ValueError("Image size exceeds the 10 MB limit")
        message = _(f"{title}\n\n{content}")
        bot.send_photo(
            user.telegram_id, news.image, caption=message, parse_mode="Markdown"
        )
    except BotUsers.DoesNotExist:
        pass
    except ValueError as e:
        logger.error(e)
