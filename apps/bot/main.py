import logging
import os

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")  # noqa

# Initialize Django
import django

django.setup()  # noqa

# Django
from apps.bot.conf import TOKEN
from apps.bot.filters import AdminFilter
from apps.bot.handlers.admin import admin_user
from apps.bot.handlers.user import any_user
from apps.bot.middlewares import antispam_func
from apps.bot.middlewares import set_language
from apps.bot.utils.database import Database
from telebot import TeleBot, apihelper
from telebot.types import InlineQueryResultPhoto

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Log a message to indicate the bot is starting
logger.info("Starting bot...")

# States
db = Database()

# Enable middlewares
apihelper.ENABLE_MIDDLEWARE = True

# I recommend increasing num_threads
bot = TeleBot(TOKEN, num_threads=5)


def register_handlers():
    bot.register_message_handler(
        admin_user, commands=["start"], admin=True, pass_bot=True
    )
    bot.register_message_handler(
        any_user, commands=["start"], admin=False, pass_bot=True
    )


register_handlers()

# Middlewares
bot.register_middleware_handler(antispam_func, update_types=["message"])
bot.register_middleware_handler(set_language, update_types=["message"])

# Custom filters
bot.add_custom_filter(AdminFilter())

concerts = [
    {
        "name": "Ochiq mikrofon",
        "date": "26.09.2024 19:00",
        "location": "SAHNA stand-up club, Yunusobod, 4-kvartal, 28A",
        "host": "Abdulaziz Hakimovich",
        "description": "Tajribali va yosh stand-up komiklar o'zlarining hazillarini sinab ko'rishadi!",
        "photo_url": "https://i.postimg.cc/GtqCnhY2/photo-2024-09-21-18-11-28.jpg",
    },
    {
        "name": "Jazz kechasi",
        "date": "01.10.2024 20:00",
        "location": "Jazz Club, Shahar markazi, 15-uy",
        "host": "Rustam Toshpo'latov",
        "description": "Eng yaxshi jazz musiqachilari ishtirokida musiqa oqshomi!",
        "photo_url": "https://i.postimg.cc/GtqCnhY2/photo-2024-09-21-18-11-28.jpg",
    },
    # Yana boshqa konsertlar qo'shilishi mumkin
]


@bot.inline_handler(func=lambda query: True)
def inline_query(query):
    results = []
    for concert in concerts:
        result = InlineQueryResultPhoto(
            id=concert["name"],
            title=concert["name"],
            description=f"{concert['date']} - {concert['location']}",
            photo_url=concert["photo_url"],
            thumbnail_url=concert["photo_url"],
            caption=(
                f"🎤 *{concert['name']}*\n\n"
                f"🗓 Sana: {concert['date']}\n"
                f"📍 Manzil: {concert['location']}\n"
                f"👤 Boshloqchi: {concert['host']}\n"
                f"📜 Tavsif: {concert['description']}"
            ),
            parse_mode="Markdown",
        )
        results.append(result)

    bot.answer_inline_query(query.id, results)


def run():
    bot.infinity_polling()


if __name__ == "__main__":
    logger.info("Bot is running...")
    logger.info("Press Ctrl + C to stop the bot")
    logger.info("====================================")
    run()
    logger.info("====================================")
