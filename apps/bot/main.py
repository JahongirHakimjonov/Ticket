import os
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")  # noqa

# Initialize Django
import django

django.setup()

# Django
import time

import requests
from apps.bot.conf import TOKEN
from apps.bot.filters import AdminFilter
from apps.bot.handlers.user import any_user
from apps.bot.middlewares import antispam_func
from apps.bot.handlers.home import handle_message
from apps.bot.middlewares import set_language
from apps.bot.utils.database import Database
from telebot import TeleBot, apihelper
from apps.bot.query import query_text
from apps.bot.logger import logger  # Import logger from the new module
from apps.bot.handlers.callback import handle_callback_query

# Log a message to indicate the bot is starting
logger.info("Starting bot...")

# States
db = Database()

# Enable middleware
apihelper.ENABLE_MIDDLEWARE = True
logger.info("Middlewares enabled")

# I recommend increasing num_threads
bot = TeleBot(TOKEN, num_threads=5)
logger.info("Bot created")


def register_handlers(bot: TeleBot):
    bot.register_message_handler(
        any_user, commands=["start"], admin=False, pass_bot=True
    )
    bot.register_message_handler(handle_message, content_types=["text"], pass_bot=True)
    bot.register_callback_query_handler(
        lambda call: handle_callback_query(call, bot), lambda call: True
    )


register_handlers(bot)
logger.info("Handlers registered")

# def handle_message_listener(messages, bot):
#     for message in messages:
#         handle_message(message, bot)
#         logger.info(f"Message from {message.from_user.id} handled")


# bot.set_update_listener(lambda messages: handle_message_listener(messages, bot))
# logger.info("Update listener set")

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
    retry_delay = 1  # Initial delay in seconds

    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except requests.exceptions.ReadTimeout:
            logger.error("Read timeout occurred. Retrying...")
        except requests.exceptions.ConnectTimeout:
            logger.error("Connection timeout occurred. Retrying in 15 seconds...")
            time.sleep(15)
        except requests.exceptions.RequestException as e:
            logger.error(
                f"Network error occurred: {e}. Retrying in {retry_delay} seconds..."
            )
            time.sleep(retry_delay)
            retry_delay = min(
                retry_delay * 2, 60
            )  # Exponential backoff, max 60 seconds
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise


if __name__ == "__main__":
    logger.info("Bot is running...")
    logger.info("Press Ctrl + C to stop the bot")
    run()
    logger.info("Bot stopped")
