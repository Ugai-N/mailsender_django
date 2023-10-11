from django.urls import path

from recipients.apps import RecipientsConfig
from recipients.views import RecipientCreateView, RecipientListView, RecipientUpdateView, RecipientDeleteView

app_name = RecipientsConfig.name
urlpatterns = [
    path('create/', RecipientCreateView.as_view(), name='create'),
    path('', RecipientListView.as_view(), name='list'),
    path('edit/<int:pk>', RecipientUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', RecipientDeleteView.as_view(), name='delete'),
]
