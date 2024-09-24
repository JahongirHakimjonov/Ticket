from telebot.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import os
from apps.bot.logger import logger
from apps.ticket.models import Concert


def query_text(bot, query):
    try:
        results = []
        concerts = Concert.objects.filter(is_active=True)
        for concert in concerts:
            thumbnail_url = f"{os.getenv('BASE_URL')}{concert.photo.url}"
            logger.info(f"Concert photo URL: {thumbnail_url}")
            keyboard = InlineKeyboardMarkup()
            button = InlineKeyboardButton(
                text="Batafsil ma'lumot",
                url=f"https://t.me/shinzo_family_bot?start={concert.id}",
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
                                 f"*📍Manzil:* {concert.address}\n"
                                 f"*💸Narxlar:* {concert.min_price} UZS - {concert.max_price} UZS\n",
                    parse_mode="Markdown",
                ),
                reply_markup=keyboard,
            )
            results.append(article_result)

        if query.from_user.id == bot.get_me().id:
            logger.info("Inline query results sent to the bot itself")
            for result in results:
                bot.send_message(
                    query.from_user.id,
                    result.input_message_content.message_text,
                    parse_mode="Markdown",
                    reply_markup=result.reply_markup,
                )
        else:
            bot.answer_inline_query(query.id, results)
        logger.info(f"Inline query results sent to {query.from_user.id}")
    except Exception as e:
        print(e)
        bot.answer_inline_query(query.id, [])
        logger.error(f"Error while answering inline query: {e}")
