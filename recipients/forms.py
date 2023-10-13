from django import forms

from recipients.models import Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        exclude = ('owner',)

