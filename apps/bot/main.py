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
from apps.bot.handlers.home import handle_message
from apps.bot.middlewares import set_language
from apps.bot.utils.database import Database
from telebot import TeleBot, apihelper
from apps.bot.query import query_text
from apps.bot.logger import logger  # Import logger from the new module

# Log a message to indicate the bot is starting
logger.info("Starting bot...")

# States
db = Database()

# Enable middlewares
apihelper.ENABLE_MIDDLEWARE = True
logger.info("Middlewares enabled")

# I recommend increasing num_threads
bot = TeleBot(TOKEN, num_threads=5)
logger.info("Bot created")


def register_handlers():
    bot.register_message_handler(
        admin_user, commands=["start"], admin=True, pass_bot=True
    )
    bot.register_message_handler(
        any_user, commands=["start"], admin=False, pass_bot=True
    )
    bot.register_message_handler(handle_message, content_types=["text"], pass_bot=True)


register_handlers()
logger.info("Handlers registered")

# Inline query
bot.register_inline_handler(
    callback=lambda query: query_text(bot, query), func=lambda query: True
)
logger.info("Inline query handler registered")

# Middlewares
bot.register_middleware_handler(antispam_func, update_types=["message"])
bot.register_middleware_handler(set_language, update_types=["message"])
logger.info("Middlewares registered")

# Custom filters
bot.add_custom_filter(AdminFilter())
logger.info("Custom filters registered")


def run():
    bot.infinity_polling()
    logger.info("Bot stopped")


if __name__ == "__main__":
    logger.info("Bot is running...")
    logger.info("Press Ctrl + C to stop the bot")
    run()
