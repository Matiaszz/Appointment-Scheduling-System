from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from ..forms.scheduling_forms import ServiceForm


class CreateSchedulingView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'form': ServiceForm()
        }
        return render(
            self.request, 'appointments/create_scheduling.html', context
        )
