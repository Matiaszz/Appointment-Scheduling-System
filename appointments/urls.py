
from django.urls import path
from appointments.views import index_view, AuthView, AccountView, logout_view

app_name = 'appointments'

urlpatterns = [
    path('', index_view, name='index'),
    path('authentication/', AuthView.as_view(), name='authentication'),
    path('account/', AccountView, name='account'),
    path('logout/', logout_view, name='logout')
]
