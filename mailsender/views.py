from apscheduler.schedulers import SchedulerAlreadyRunningError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailsender.forms import MessageForm, MailForm
from mailsender.models import Message, Mail
from mailsender.services import scheduler, run_APScheduler


class MessageListView(ListView):
    paginate_by = 3
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailsender:message_list')

    # def get_success_url(self):
    #     return reverse('mailsender:message_detail', args=[self.kwargs.get('pk')])


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailsender:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailsender:message_list')


# OK
class MailListView(ListView):
    paginate_by = 5
    model = Mail


# NO NEED
# class MailDetailView(DetailView):
#     model = Mail


class MailCreateView(CreateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailsender:mail_list')


class MailUpdateView(UpdateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailsender:mail_list')


class MailDeleteView(DeleteView):
    model = Mail
    success_url = reverse_lazy('mailsender:mail_list')


def toggle_mail_activity(request, pk):
    mail_item = get_object_or_404(Mail, pk=pk)
    job_id = f"{pk}:{mail_item.title}" #или записыватьего в поле мэйл

    try:
        scheduler.start()
    except SchedulerAlreadyRunningError:
        print('Scheduler Already Running')
    # scheduler.print_jobs()

    if mail_item.activity == 'draft':
        mail_item.activity = 'active'

        # if mail_item.frequency == 'ONCE':
        #     # fr_trigger = DateTrigger(run_date=date)
        #     month = date.month
        #     day = date.day
        #     weekday = date.weekday()
        # elif mail_item.frequency == 'WEEKLY':
        #     # fr_trigger = CronTrigger(day="*/7", hour=mail_item.time.hour, minute=mail_item.time.minute, start_date=date)
        #     # fr_trigger = CronTrigger.from_crontab(f'{mail_item.time.minute} {mail_item.time.hour} * * {date.weekday()}')
        #     weekday = date.weekday()
        # # elif mail_item.frequency == 'DAILY':
        #     # fr_trigger = CronTrigger(day="*", hour=mail_item.time.hour, minute=mail_item.time.minute, start_date=date)
        #     # fr_trigger = CronTrigger.from_crontab(f'{mail_item.time.minute} {mail_item.time.hour} * * *')
        # elif mail_item.frequency == 'MONTHLY':
        #     # fr_trigger = CronTrigger(day=1, hour=mail_item.time.hour, minute=mail_item.time.minute, start_date=date)
        #     # fr_trigger = CronTrigger.from_crontab(f'{mail_item.time.minute} {mail_item.time.hour} {date.day} * *')
        #     day = date.day
        # fr_trigger = CronTrigger.from_crontab(f'{mail_item.time.minute} {mail_item.time.hour} {day} {month} {weekday}')

        run_APScheduler(job=job_id, mail_item=mail_item)
    ###############################################
    # management.call_command('runapscheduler',
    #                         email=['777ugay@gmail.com'],
    #                         title=mail_item.message.title,
    #                         message=mail_item.message.content,
    #                         trigger=fr_trigger
    #                         )
    elif mail_item.activity == 'active':
        mail_item.activity = 'paused'
        # scheduler.remove_job(job_id)
        scheduler.pause_job(job_id)

    elif mail_item.activity == 'paused':
        mail_item.activity = 'active'
        scheduler.resume_job(job_id)

    mail_item.save()
    return redirect(reverse('mailsender:mail_list'))
