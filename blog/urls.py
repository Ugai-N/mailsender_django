from django.urls import path
from django.views.decorators.cache import never_cache

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('view/<slug:slug>', ArticleDetailView.as_view(), name='article_detail'),
]
