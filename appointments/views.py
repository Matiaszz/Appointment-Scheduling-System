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


def index_view(request):
    return render(request, context={
        'title': 'Início'
    }, template_name='appointments/index.html')


def our_services_view(request):
    return render(request,
                  context={
                      'title': 'Nossos Serviços'
                  },
                  template_name='appointments/our_services.html')


def custom_403_view(request, exception):
    return render(
        request, 'error.html',
        context={
            'error_code': 403,
            'title': 'Proibido'

        }, status=403)


def custom_404_view(request, exception):
    return render(
        request, 'error.html',
        context={
            'error_code': 404,
            'title': 'Página não encontrada'

        }, status=404)
