from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailsender.forms import MessageForm, MailForm
from mailsender.models import Message, Mail


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
