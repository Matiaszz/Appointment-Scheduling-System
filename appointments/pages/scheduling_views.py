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
            return redirect('appointments:schedules')

        messages.error(request, 'Não foi possível agendar')
        return render(request, 'appointments/create_scheduling.html',
                      {'form': form})


class ReadSchedulingView(LoginRequiredMixin, ListView):
    template_name = 'appointments/my_schedules.html'
    paginate_by = 10

    def get_queryset(self):
        """
        Retrieves the schedules from an external API and filters them by
        the logged-in user.
        """
        api_url = os.getenv('SCHEDULES_API_URL')

        if not api_url:
            messages.error(self.request, 'URL da API não está configurada.')
            return []

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            schedules = response.json().get('results', [])

            user_id = self.request.user.pk
            filtered_schedules = [
                item for item in schedules if item['client'] == user_id
            ]
            return filtered_schedules

        except requests.exceptions.RequestException as e:
            messages.error(
                self.request, f'Erro ao pegar informações: {str(e)}')
            return []

    def get(self, *args, **kwargs):
        """
        Handles GET requests to fetch and display the list of schedules.
        """
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Scheduling.objects.all().order_by('-pk')
    serializer_class = ScheduleSerializer
