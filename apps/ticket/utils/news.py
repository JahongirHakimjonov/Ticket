from celery import shared_task
from telebot.apihelper import ApiTelegramException

from apps.bot.utils.send_message import send_news
from apps.ticket.models import News, BotUsers


@shared_task()
def send_news_to_subscribers(news_id):
    try:
        news = News.objects.get(id=news_id)
        users = BotUsers.objects.all()
        for user in users:
            try:
                send_news(user.id, news.title, news.content, news.image, news_id)
            except ApiTelegramException as e:
                if e.error_code == 403:
                    print(f"User {user.id} has blocked the bot.")
                    # Optionally, remove the user from the subscribers list
                    user.is_active = False
                    user.save()
                else:
                    print(f"An error occurred: {e}")
    except News.DoesNotExist:
        print(f"News with id {news_id} does not exist.")
    except Exception as exc:
        print(f"An error occurred: {exc}")
