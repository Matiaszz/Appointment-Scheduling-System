from django import forms
from django.core.exceptions import ValidationError
from ..models import Scheduling
from datetime import time, timedelta
from django.utils import timezone
from ..services.google_calendar_service import insert_into_calendar


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
            if timezone.is_naive(date_time):
                date_time = timezone.make_aware(date_time)

            if date_time < timezone.now():
                raise ValidationError(
                    'A data e hora do agendamento não podem ser no passado.'
                )

            if not (time(7, 0) <= date_time.time() <= time(17, 0)):
                raise ValidationError(
                    'O agendamento deve ser feito durante o horário comercial '
                    '(07:00 - 17:00).'
                )

            if date_time < timezone.now() + timedelta(minutes=30):
                raise ValidationError(
                    'O agendamento deve ser feito com pelo menos 30 minutos '
                    'de antecedência.'
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

            end_time = date_time + timedelta(minutes=service.duration)

            conflicting_scheduling = Scheduling.objects.filter(
                service=service,
                date_time__lt=end_time,
                date_time__gt=date_time,
                status='active'
            )

            if conflicting_scheduling.exists():
                raise ValidationError(
                    'O horário solicitado conflita com outro agendamento ativo'
                    ' para este serviço.'
                )

            if not insert_into_calendar(
                summary=service.service_name,
                start=date_time,
                end=end_time,
                description=cleaned_data.get('notes', '')
            ):
                raise ValidationError(
                    'Erro ao inserir o agendamento no calendário.'
                )

        return cleaned_data
