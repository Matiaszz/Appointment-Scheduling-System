from django.shortcuts import redirect, render
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms.barber_forms import ServiceForm
from ..models import BarberService
from rest_framework import viewsets
from ..serializers import ServiceSerializer
from dotenv import load_dotenv
import requests
import os
import logging

logger = logging.getLogger(__name__)

load_dotenv('.../env/.env')


class ServicesView(LoginRequiredMixin, View):
    def get(self, request):
        if (
            (request.user.user_type != 'employee') and
            (request.user.user_type != 'superuser')
        ):
            return redirect('appointments:index')

        service_form = ServiceForm

        context = {
            'service_form': service_form
        }

        return render(self.request, 'appointments/services.html', context)

    def post(self, request):
        service_form = ServiceForm(request.POST, request.FILES)

        if service_form.is_valid():
            print("Dados limpos:", service_form.cleaned_data)
            service = service_form.save(commit=False)
            service.save()
            return redirect('appointments:services_list')

        print("Erros do formulário:", service_form.errors)
        context = {'service_form': service_form}
        return render(self.request, 'appointments/services.html', context)


class ServicesListView(LoginRequiredMixin, ListView):
    model = BarberService
    template_name = 'appointments/services_list.html'

    def get(self, request):
        api_url = str(os.getenv('API_URL'))

        response = requests.get(api_url)
        services = response.json()
        context = {
            'obj': services,
        }
        return render(self.request, self.template_name, context)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = BarberService.objects.all()
    serializer_class = ServiceSerializer
