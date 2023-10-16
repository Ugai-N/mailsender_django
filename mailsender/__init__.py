# import django
# from django.apps import AppConfig
# from django.contrib.sites.models import Site
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
#
# from mailsender.services import scheduler
# django.setup()
# class MailsenderConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#
#
# name = 'mailsender'
# verbose_name = 'Сервис рассылок'
#
#
# def ready(self):
#         # importing model classes
#     from .models import Mail
#
#         # registering signals with the model's string label
#     pre_save.connect(receiver, sender='app_label.Mail')
#
#
#
