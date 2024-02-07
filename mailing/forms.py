from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms

from client.models import Client
from mailing.models import MailingMessage, MailingSettings


class MailingMessageForm(forms.ModelForm):
    class Meta:
        model = MailingMessage
        exclude = ['owner']

    def __init__(self, user, *args, **kwargs, ):
        self.user = user
        super(MailingMessageForm, self).__init__(*args, **kwargs)

        if user.is_superuser:
            self.fields['client'].queryset = Client.objects.all()
        else:
            self.fields['client'].queryset = Client.objects.filter(owner=user)
        for field_name, field in self.fields.items():
            if field_name != 'is_active_mail':
                field.widget.attrs['class'] = 'form-control'

class MailingSettingsForm(forms.ModelForm):

    class Meta:
        model = MailingSettings
        fields = ('period_choices', 'start_date', 'stop_date')

        # widgets = {
        #     'start_date': DatePickerInput(),
        #     'stop_date': DatePickerInput(),
        # }

    def clean(self):
        # try:
            cleaned_data_start = self.cleaned_data['start_date']
            cleaned_data_stop = self.cleaned_data['stop_date']
            if cleaned_data_start >= cleaned_data_stop:
                raise forms.ValidationError('Введите правильно даты начала и конца рассылки')
        # except KeyError:
        #     forms.ValidationError('Поля обязательны к заполнению')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not isinstance(field, forms.DateField):
                field.widget.attrs['class'] = 'form-control'


