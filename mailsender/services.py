import smtplib

from apscheduler.schedulers import SchedulerAlreadyRunningError
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from mailsender.models import Try
import logging

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
scheduler.add_jobstore(DjangoJobStore(), "default")


#варианты отправки массовых писем со скрытыми адресами https://mailtrap.io/blog/django-send-email/
def send_message(email, title, message):
    send_mail(
        subject=title,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=email)


def create_try(mail_item):
    emails_list = []
    for cat in mail_item.category.all():
        emails_list.extend([person.email for person in cat.recipient_set.all()])
    emails_list = list(set(emails_list))

    try:
        # print(f"recipients:{emails_list}\ntitle:{mail_item.message.title}\nmessage:{mail_item.message.content}")
        send_message(emails_list, mail_item.message.title, mail_item.message.content)
        Try.objects.create(mail=mail_item, status=True)
    # except OSError as error:
    except smtplib.SMTPException as error:
        Try.objects.create(mail=mail_item, status=False, error_message=error)


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def run_APScheduler(job, mail_item):
    day = weekday = month = '*'
    # date = datetime.combine(mail_item.start_date, mail_item.time)
    if mail_item.frequency == 'ONCE':
        month = mail_item.start_date.month
        day = mail_item.start_date.day
        weekday = mail_item.start_date.weekday()
    elif mail_item.frequency == 'WEEKLY':
        weekday = mail_item.start_date.weekday()
    elif mail_item.frequency == 'MONTHLY':
        day = mail_item.start_date.day
    trigger = CronTrigger.from_crontab(f'{mail_item.time.minute} {mail_item.time.hour} {day} {month} {weekday}')

    ##########################
    scheduler.add_job(
        create_try,
        trigger,
        args=[mail_item],
        id=job,
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'create_log'.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
        ),  # Midnight on Monday, before start of the next work week.
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    logger.info(
        "Added weekly job: 'delete_old_job_executions'."
    )

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except SchedulerAlreadyRunningError:
        logger.info("scheduler is already running!")
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")
