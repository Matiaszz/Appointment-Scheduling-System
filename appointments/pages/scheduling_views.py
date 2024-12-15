from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from ..forms.scheduling_forms import ScheduleForm
from django.contrib import messages


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
