import os

from telebot.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from apps.bot.logger import logger
from apps.ticket.models import Concert
from django.utils.translation import activate, gettext as _


def query_text(bot, query):
    try:
        results = []
        concerts = Concert.objects.filter(is_active=True)
        for concert in concerts:
            thumbnail_url = f"{os.getenv('BASE_URL')}{concert.photo.url}"
            keyboard = InlineKeyboardMarkup()
            button = InlineKeyboardButton(
                text="Sotib olish",
                url=f"{os.getenv('BOT_URL')}?start={concert.id}",
            )
            keyboard.add(button)
            article_result = InlineQueryResultArticle(
                id=concert.id,
                title=concert.name,
                description=f"{concert.date.strftime('%d.%m.%Y')} {concert.time.strftime('%H:%M')}",
                thumbnail_url=thumbnail_url,
                input_message_content=InputTextMessageContent(
                    message_text=f"{concert.name}\n\n{concert.title}\n\n"
                    f"{concert.date.strftime('%d.%m.%Y')} {concert.time.strftime('%H:%M')}\n\n"
                    f"{concert.description}\n\n[ ]({thumbnail_url})\n"
                    f"*📍Manzil \ Адрес:* {concert.address}\n"
                    f"*💸Narxlar \ Цены:* {concert.min_price:,} UZS - {concert.max_price:,} UZS\n",
                    parse_mode="Markdown",
                ),
                reply_markup=keyboard,
            )
            results.append(article_result)
        bot.answer_inline_query(query.id, results)
        logger.info(f"Inline query results sent to {query.from_user.id}")
    except Exception as e:
        bot.answer_inline_query(query.id, [])
        logger.error(f"Error while answering inline query: {e}")
