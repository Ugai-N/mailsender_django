from django.apps import AppConfig
# from django.conf import settings
#
# from mailsender.services import scheduler


class MailsenderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailsender'
    verbose_name = 'Сервис рассылок'


# def start_scheduler():
#     if settings.SCHEDULER_AUTOSTART:
#         try:
#             scheduler.start()
#         except KeyboardInterrupt:
#             scheduler.shutdown()
