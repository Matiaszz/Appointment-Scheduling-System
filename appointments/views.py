"""
Static pages, with only frontend.

This module contains views for rendering static pages of the application.

Parameters
----------
request : HttpRequest
    The request object containing metadata about the request.

Returns
-------
HttpResponse
    Render the requested static page.
"""
from django.shortcuts import render
from .models import Scheduling
from django.contrib.auth.decorators import login_required


def index_view(request):
    return render(request, 'appointments/index.html')


def our_services_view(request):
    return render(request, 'appointments/our_services.html')


@login_required
def my_schedules_view(request):
    items = Scheduling.objects.filter(client=request.user)
    context = {
        'items': items
    }
    return render(request, 'appointments/my_schedules.html', context)
