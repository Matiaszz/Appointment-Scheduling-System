from django import forms
from ..models import BarberService


class ServiceForm(forms.ModelForm):
    class Meta:

        model = BarberService
        fields = ['service_name', 'price', 'service_type', 'description',
                  'image', 'is_active', 'duration']
