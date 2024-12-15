from django import forms
from django.core.exceptions import ValidationError
from ..models import Scheduling
from datetime import time


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Scheduling
        fields = ['service', 'date_time', 'notes']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')

        if date_time:
            if not (time(7, 0) <= date_time.time() <= time(17, 0)):
                raise ValidationError(
                    'O agendamento deve ser feito durante o horário comercial '
                    '(07:00 - 17:00).'
                )
        return date_time

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        date_time = cleaned_data.get('date_time')

        if service and date_time:
            existing_scheduling = Scheduling.objects.filter(
                service=service,
                date_time=date_time,
                status='active'
            )

            if existing_scheduling.exists():
                raise ValidationError(
                    'Já existe um agendamento para este serviço e horário. '
                    'Por favor, escolha outro horário.'
                )
        return cleaned_data
