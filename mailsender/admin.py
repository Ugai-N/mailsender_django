from django.contrib import admin

from blog.models import Article
from mailsender.models import Message, Mail, Try
from recipients.models import Recipient, Category


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('owner', 'first_name', 'middle_name', 'last_name', 'email', 'notes',)
    list_filter = ('owner', 'category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'description',)
    list_filter = ('owner', 'mail',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'content',)
    list_filter = ('mail', 'owner')
    search_fields = ('title', 'content',)


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('owner', 'job_id', 'title', 'message', 'start_date', 'time', 'frequency', 'activity', 'created_at', 'updated_at', )
    list_filter = ('owner', 'activity', 'category', 'message',)


@admin.register(Try)
class TryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'launched_at', 'status', 'mail', 'error_message',)
    list_filter = ('status', 'mail',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'content', 'created_at', 'is_published', 'published_at', 'views_count', 'preview', )
    list_filter = ('owner', 'is_published',)
    search_fields = ('title', 'content')
