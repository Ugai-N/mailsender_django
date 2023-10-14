from django.core.management import BaseCommand

from mailsender.models import Mail
from mailsender.services import run_APScheduler


class Command(BaseCommand):

    def handle(self, *args, **options):
        all_mails = Mail.objects.filter(activity='draft') | Mail.objects.filter(activity='paused')
        for mail_item in all_mails:
            run_APScheduler(mail_item)
            mail_item.activity = 'active'
            mail_item.save()
