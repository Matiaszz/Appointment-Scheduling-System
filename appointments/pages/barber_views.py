from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib import messages
from ..forms.barber_forms import ServiceForm


class ServicesView(View):
    def get(self, request):
        service_form = ServiceForm
        context = {
            'service_form': service_form
        }
        return render(self.request, 'appointments/services.html', context)
