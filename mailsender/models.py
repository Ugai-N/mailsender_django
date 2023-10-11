from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mail(models.Model):
    ACTIVITY_CHOICES = [
        ('draft', 'черновик'),
        ('paused', 'приостановлена'),
        ('active', 'активна'),
    ]
    FREQUENCY_CHOICES = [
        ('WEEKLY', 'Раз в неделю'),
        ('MONTHLY', 'Раз в месяц'),
        ('DAILY', 'Раз в день'),
        ('ONCE', 'Разово'),
    ]
    title = models.CharField(max_length=100, verbose_name='название рассылки')
    time = models.TimeField(verbose_name='время отправки')
    start_date = models.DateField(verbose_name='дата отправки (старта)', default=timezone.now())
    activity = models.CharField(max_length=100, choices=ACTIVITY_CHOICES, default='draft', verbose_name='активность')
    frequency = models.CharField(max_length=150, choices=FREQUENCY_CHOICES, verbose_name='периодичность', default='ONCE')
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='выбрать сообщение')
    # category = models.ManyToManyField('recipients.Category', verbose_name='категория получателей')
    created_at = models.DateField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата изменения')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Try(models.Model):
    status = models.BooleanField(verbose_name='статус', default=False)
    error_message = models.TextField(verbose_name='отчет об ошибке', **NULLABLE)
    mail = models.ForeignKey('Mail', on_delete=models.CASCADE, verbose_name='рассылка')
    launched_at = models.DateTimeField(auto_now=True, verbose_name='время запуска')

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'
