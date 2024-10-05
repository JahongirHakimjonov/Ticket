from celery import shared_task

from apps.bot.utils.send_message import send_news
from apps.ticket.models import News, BotUsers


@shared_task()
def send_news_to_subscribers(news_id):
    try:
        news = News.objects.get(id=news_id)
        users = BotUsers.objects.all()
        for user in users:
            send_news(user.id, news.title, news.content, news.image, news_id)
    except News.DoesNotExist:
        print(f"News with id {news_id} does not exist.")
    except Exception as exc:
        print(f"An error occurred: {exc}")
