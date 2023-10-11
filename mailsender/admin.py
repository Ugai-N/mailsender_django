from django.contrib import admin

from mailsender.models import Message, Mail, Try
from recipients.models import Recipient, Category


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'email', 'notes',)
    list_filter = ('category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    list_filter = ('mail',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'content',)
    list_filter = ('mail',)
    search_fields = ('title', 'content',)


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'start_date', 'time', 'frequency', 'activity', 'created_at', 'updated_at', )
    # list_filter = ('activity', 'category', 'message',)
    list_filter = ('activity', 'message',)


@admin.register(Try)
class TryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'launched_at', 'status', 'mail', 'error_message',)
    list_filter = ('status', 'mail',)
