from django.shortcuts import render
app_name = 'appointments'


def index_view(request):
    return render(request, 'appointments/index.html')


def our_services_view(request):
    return render(request, 'appointments/our_services.html')
