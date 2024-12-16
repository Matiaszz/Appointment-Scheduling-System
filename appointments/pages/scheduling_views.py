import os
import requests
from rest_framework import viewsets
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View, ListView
from ..forms.scheduling_forms import ScheduleForm
from ..utils.others import get_env
from ..models import Scheduling
from ..serializers import ScheduleSerializer
get_env()


class CreateSchedulingView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'form': ScheduleForm()
        }
        return render(
            request, 'appointments/create_scheduling.html', context
        )

    def post(self, request):
        form = ScheduleForm(request.POST)

        if form.is_valid():
            scheduling = form.save(commit=False)
            scheduling.client = request.user
            scheduling.save()
            messages.success(request, 'Agendado com sucesso.')
            return redirect('appointments:account')

        messages.error(request, 'Não foi possível agendar')
        return render(request, 'appointments/create_scheduling.html',
                      {'form': form})


class ReadSchedulingView(LoginRequiredMixin, ListView):
    template_name = 'appointments/my_schedules.html'

    def get(self, request):
        """
        Handles GET requests to fetch and display the list of schedules.

        Retrieves the services from an external API and renders them in the
        services list template.

        Parameters
        ----------
        request : HttpRequest
            The request object containing metadata about the request.

        Returns
        -------
        HttpResponse
            Renders the services list template with the fetched services.
        """
        api_url = str(os.getenv('SCHEDULES_API_URL'))
        response = requests.get(api_url)

        if response.status_code == 200:
            user_id = request.user.id
            schedules = response.json().get('results', [])
            filtered_schedules = [
                item for item in schedules if item['client'] == user_id
            ]

            context = {
                'items': filtered_schedules,
            }
            return render(self.request, self.template_name, context)

        messages.error(request, 'Erro ao carregar os agendamentos.')
        return redirect('appointments:index')


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Scheduling.objects.all()
    serializer_class = ScheduleSerializer
