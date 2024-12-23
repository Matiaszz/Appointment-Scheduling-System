import os
from rest_framework import viewsets
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, ListView
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from ..forms.scheduling_forms import ScheduleForm
from ..utils.others import get_env
from ..utils.api import get_results_api
from ..models import Scheduling
from ..serializers import ScheduleSerializer
from ..services.google_calendar_service import (
    insert_into_calendar, delete_from_calendar
)
get_env()


class CreateSchedulingView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'form': ScheduleForm(),
            'title': 'Criar Agendamento',

        }
        return render(
            request, 'appointments/create_scheduling.html', context
        )

    def post(self, request):
        form = ScheduleForm(request.POST)

        if form.is_valid():
            scheduling = form.save(commit=False)
            scheduling.client = request.user
            start_time = scheduling.date_time
            end_time = start_time + \
                timezone.timedelta(minutes=scheduling.service.duration)

            created_event = insert_into_calendar(
                summary=scheduling.service.service_name,
                start=start_time,
                end=end_time,
                description=form.cleaned_data.get('notes', '')
            )

            if not created_event:
                raise Exception(
                    'Erro ao inserir o agendamento na Agenda.')

            scheduling.calendar_event_id = created_event['id']
            scheduling.save()

            messages.success(request, 'Agendado com sucesso.')
            return redirect('appointments:schedules')

        messages.error(request, 'Não foi possível agendar')
        return render(request, 'appointments/create_scheduling.html',
                      {'form': form})


class ListSchedulesView(LoginRequiredMixin, ListView):
    template_name = 'appointments/my_schedules.html'
    paginate_by = 10

    def get_queryset(self):
        """
        Retrieves the schedules from an external API and filters them by
        the logged-in user.
        """
        api_url = os.getenv('SCHEDULES_API_URL')

        schedules = get_results_api(self.request, api_url)

        user_id = self.request.user.pk
        filtered_schedules = [
            item for item in schedules if item['client'] == user_id
        ]
        return filtered_schedules

    def get(self, *args, **kwargs):
        """
        Handles GET requests to fetch and display the list of schedules.
        """
        self.object_list = self.get_queryset()
        context = self.get_context_data(
            object_list=self.object_list, title='Meus Agendamentos')
        return self.render_to_response(context)


class DetailScheduleView(LoginRequiredMixin, View):
    """
    Displays the details of a user's schedule. Only the client associated with
    the schedule can view it.
    """
    template_name = 'appointments/view_my_schedule.html'

    def get(self, request, schedule_id):
        """
        Handles the GET request to display the schedule details.

        Args:
            request: The HTTP request object.
            schedule_id: The ID of the schedule to be displayed.

        Returns:
            HttpResponse: The rendered schedule details page.

        Raises:
            PermissionDenied: If a user tries to access another client's
            schedule.
        """

        user = request.user
        existing_schedule = get_object_or_404(Scheduling, pk=schedule_id)

        if ((existing_schedule.client != user) and user.is_client()):
            raise PermissionDenied(
                'You dont have permission to access this page.')

        context = {
            'schedule_id': schedule_id,
            'schedule': existing_schedule,
            'title': 'Agendamento',

        }
        return render(request, self.template_name, context)


class UpdateScheduleView(LoginRequiredMixin, View):
    """
    Allows users to update their schedule details. Only the client associated
    with the schedule can update it.
    """
    template_name = 'appointments/update_schedule.html'

    def get(self, request, schedule_id):
        """
        Handles the GET request to display the schedule update form.

        Args:
            request: The HTTP request object.
            schedule_id: The ID of the schedule to be updated.

        Returns:
            HttpResponse: The rendered schedule update page.

        Raises:
            PermissionDenied: If a user tries to update another client's
            schedule.
        """
        existing_schedule = get_object_or_404(Scheduling, pk=schedule_id)

        if ((existing_schedule.client != request.user) and
                request.user.is_client()):
            raise PermissionDenied(
                'You dont have permission to access this page.')

        new_date_time = existing_schedule.date_time - timezone.timedelta(
            hours=3)
        formatted_date_time = new_date_time.strftime('%Y-%m-%dT%H:%M')
        initial_data = {
            'service': existing_schedule.service,
            'date_time': formatted_date_time,
            'notes': existing_schedule.notes,
        }

        form = ScheduleForm(initial=initial_data)

        context = {
            'title': 'Atualizar Agendamento',
            'form': form,
            'schedule_id': schedule_id,

        }

        return render(request, self.template_name, context)

    def post(self, request, schedule_id):
        """
        Handles the POST request to save the updated schedule details.

        Args:
            request: The HTTP request object.
            schedule_id: The ID of the schedule to be updated.

        Returns:
            HttpResponse: A redirect to the schedule list or the same page
            with error messages.
        """
        existing_schedule = get_object_or_404(Scheduling, pk=schedule_id)

        form = ScheduleForm(request.POST, instance=existing_schedule)

        if form.is_valid():
            try:
                with transaction.atomic():
                    if existing_schedule.calendar_event_id:
                        delete_from_calendar(
                            existing_schedule.calendar_event_id)

                    scheduling = form.save(commit=False)
                    scheduling.save()

                    start_time = scheduling.date_time
                    end_time = start_time + \
                        timezone.timedelta(minutes=scheduling.service.duration)

                    created_event = insert_into_calendar(
                        summary=scheduling.service.service_name,
                        start=start_time,
                        end=end_time,
                        description=form.cleaned_data.get('notes', '')
                    )

                    if not created_event:
                        raise Exception(
                            'Erro ao inserir o agendamento na Agenda.')

                    scheduling.calendar_event_id = created_event['id']
                    scheduling.save()

                messages.success(
                    request, 'Agendamento atualizado com sucesso.')

                return redirect('appointments:schedules')

            except Exception as e:
                messages.error(request, f'Ocorreu um erro: {e}')

        return render(request, self.template_name,
                      {'form': form, 'schedule_id': schedule_id})


class DeleteScheduleView(LoginRequiredMixin, View):
    """
    Allows users to delete their schedules. Only the client associated with
    the schedule can delete it.
    """

    def post(self, request, schedule_id):
        """
        Handles the POST request to delete a schedule.

        Args:
            request: The HTTP request object.
            schedule_id: The ID of the schedule to be deleted.

        Returns:
            HttpResponse: A redirect to the schedule list or an error page.
        """
        existing_schedule = get_object_or_404(Scheduling, pk=schedule_id)

        if ((existing_schedule.client != request.user) and
                request.user.is_client()):
            return render(request, '404.html', status=404)

        try:
            with transaction.atomic():
                if existing_schedule.calendar_event_id:
                    delete_from_calendar(
                        existing_schedule.calendar_event_id)

                existing_schedule.delete()
                messages.success(request, 'Agendamento deletado')

                return redirect('appointments:schedules')

        except Exception as e:
            messages.error(request, f'Um erro ocorreu: {e}')


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    API viewset for managing schedule objects. Allows CRUD operations on
    schedules via API.
    """
    queryset = Scheduling.objects.all().order_by('-pk')
    serializer_class = ScheduleSerializer
