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
app_name = 'appointments'


def index_view(request):
    return render(request, 'appointments/index.html')


def our_services_view(request):
    return render(request, 'appointments/our_services.html')
