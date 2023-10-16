from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailsender.views import OwnerRequiredMixin
from recipients.forms import RecipientForm
from recipients.models import Recipient


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient

    def get_queryset(self, *args, **kwargs):
        """Если не персонал, то выводим только принадлежащие автору объекты"""
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('recipients:list')

    def form_valid(self, form):
        """При создании получателя, записываем автора-пользователя в атрибуты объекта"""
        if form.is_valid():
            form.instance.owner = self.request.user
            form.save()
        return super().form_valid(form)


# наверное при редактировании адреса почты нужно модифицировать джобу???
class RecipientUpdateView(OwnerRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('recipients:list')


# наверное при удалении нужно модифицировать джобу???
class RecipientDeleteView(OwnerRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy('recipients:list')
