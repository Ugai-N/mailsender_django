from django.urls import path

from mailsender.apps import MailsenderConfig
from mailsender.views import MessageCreateView, MessageListView, MessageUpdateView, MessageDetailView, \
    MessageDeleteView, MailCreateView, MailListView, MailUpdateView, MailDeleteView, toggle_mail_activity

app_name = MailsenderConfig.name
urlpatterns = [
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('message_list', MessageListView.as_view(), name='message_list'),
    path('edit_message/<int:pk>', MessageUpdateView.as_view(), name='edit_message'),
    path('view_message/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('delete_message/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),

    path('create_mail/', MailCreateView.as_view(), name='create_mail'),
    path('mail_list', MailListView.as_view(), name='mail_list'),
    path('edit_mail/<int:pk>', MailUpdateView.as_view(), name='edit_mail'),
    path('delete_mail/<int:pk>', MailDeleteView.as_view(), name='delete_mail'),
    path('activity/<int:pk>/', toggle_mail_activity, name='toggle_mail_activity'),
]
