from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from recipients.models import Recipient


class RecipientListView(ListView):
    model = Recipient


class RecipientCreateView(CreateView):
    model = Recipient
    fields = ('first_name', 'last_name', 'middle_name', 'email', 'notes', 'category')
    success_url = reverse_lazy('recipients:list')


class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ('first_name', 'last_name', 'middle_name', 'email', 'notes', 'category')
    success_url = reverse_lazy('recipients:list')


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy('recipients:list')
