import smtplib
from datetime import timedelta, datetime, date

from apscheduler.schedulers import SchedulerAlreadyRunningError
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from mailsender.models import Try, Mail
import logging

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
scheduler.add_jobstore(DjangoJobStore(), "default")


# варианты отправки массовых писем со скрытыми адресами https://mailtrap.io/blog/django-send-email/
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
        Try.objects.create(mail=mail_item, status=True, owner=mail_item.owner)
    # except OSError as error:
    except smtplib.SMTPException as error:
        Try.objects.create(mail=mail_item, status=False, error_message=error, owner=mail_item.owner)


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


def get_job_params(mail_item):
    day = weekday = month = '*'
    stop_date = None

    send_datetime = datetime.combine(mail_item.start_date, mail_item.time)
    if send_datetime <= datetime.now():
        send_datetime = datetime.now() + timedelta(minutes=5)
        mail_item.start_date = send_datetime.date()
        mail_item.time = send_datetime.time()

    if mail_item.frequency == 'ONCE':
        month = mail_item.start_date.month
        day = mail_item.start_date.day
        weekday = mail_item.start_date.weekday()
        stop_date = mail_item.start_date + timedelta(hours=1)
    elif mail_item.frequency == 'WEEKLY':
        weekday = mail_item.start_date.weekday()
    elif mail_item.frequency == 'MONTHLY':
        day = mail_item.start_date.day
    trigger = CronTrigger.from_crontab(f'{mail_item.time.minute} {mail_item.time.hour} {day} {month} {weekday}')
    return trigger, stop_date


def run_APScheduler(mail_item):
    trigger = get_job_params(mail_item)[0]
    stop_date = get_job_params(mail_item)[1]
    # day = weekday = month = '*'
    # stop_date = None
    #
    # send_datetime = datetime.combine(mail_item.start_date, mail_item.time)
    # if send_datetime <= datetime.now():
    #     send_datetime = datetime.now() + timedelta(minutes=5)
    #     mail_item.start_date = send_datetime.date()
    #     mail_item.time = send_datetime.time()
    #
    # if mail_item.frequency == 'ONCE':
    #     month = mail_item.start_date.month
    #     day = mail_item.start_date.day
    #     weekday = mail_item.start_date.weekday()
    #     stop_date = mail_item.start_date + timedelta(hours=1)
    # elif mail_item.frequency == 'WEEKLY':
    #     weekday = mail_item.start_date.weekday()
    # elif mail_item.frequency == 'MONTHLY':
    #     day = mail_item.start_date.day
    # trigger = CronTrigger.from_crontab(f'{mail_item.time.minute} {mail_item.time.hour} {day} {month} {weekday}')

    ##########################
    scheduler.add_job(
        create_try,
        trigger,
        args=[mail_item],
        id=str(mail_item.job_id),
        max_instances=1,
        replace_existing=True,
        end_date=stop_date
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
        # for mail_item in Mail.objects.all():
        #     mail_item.activity = 'draft'
        scheduler.shutdown()

        logger.info("Scheduler shut down successfully!")


def run_job_update(mail_item):
    job_trigger = get_job_params(mail_item)[0]
    stop_date = get_job_params(mail_item)[1]
    params = {
        "trigger": job_trigger,
        "end_date": stop_date,
        'args': [mail_item], }
    scheduler.modify_job(
        job_id=str(mail_item.job_id),
        kwargs=params
    )
