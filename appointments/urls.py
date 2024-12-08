
from django.urls import path
from appointments.views import test_view

app_name = 'appointments'

urlpatterns = [
    path('', test_view, name='index'),
]
