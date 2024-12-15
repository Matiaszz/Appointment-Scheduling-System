from django import forms
from ..models import Scheduling


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Scheduling
        fields = ['service', 'date_time',
                  'notes']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
