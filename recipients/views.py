from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailsender.views import OwnerRequiredMixin
from recipients.forms import RecipientForm
from recipients.models import Recipient


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('recipients:list')

    def form_valid(self, form):
        if form.is_valid():
            form.instance.owner = self.request.user
            form.save()
        return super().form_valid(form)


class RecipientUpdateView(OwnerRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('recipients:list')


class RecipientDeleteView(OwnerRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy('recipients:list')
