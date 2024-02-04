from app_crontab.crontab_send import mailings_month
from django.core.management import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        mailings_month()
