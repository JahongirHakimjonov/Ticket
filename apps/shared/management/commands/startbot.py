from django.core.management.base import BaseCommand

from apps.bot.main import run


class Command(BaseCommand):
    help = "Starts the Telegram bot."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting the Telegram bot..."))
        self.stdout.write(self.style.SUCCESS("Telegram bot started successfully."))
        run()
        self.stdout.write(self.style.ERROR("Telegram bot stopped."))
