from django import forms

from mailsender.models import Mail, Message


class MailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        uid = kwargs.pop('uid')
        super().__init__(*args, **kwargs)
        self.fields['message'].queryset = Message.objects.all().filter(owner=uid)
        self.fields['category'].queryset = Message.objects.all().filter(owner=uid)

    class Meta:
        model = Mail
        exclude = ('activity', 'owner')
    #
    # new_message_title = forms.CharField(max_length=100, required=False, label="или СОЗДАТЬ новое сообщение с заголовком:")
    # new_message_content = forms.CharField(max_length=3000, required=False, label="и содержанием:")

    # def clean_email(self):
    #     cleaned_data = self.cleaned_data.get('email')
    #     if 'sky.pro' not in cleaned_data:
    #         raise forms.ValidationError('not skypro email')
    #     return cleaned_data


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)

