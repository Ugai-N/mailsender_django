# Generated by Django 4.2.6 on 2023-10-16 16:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mailsender', '0010_mail_stop_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='stop_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='дата завершения'),
        ),
    ]
