"""
This module defines the URL routes for the 'appointments' app.
The URLs map HTTP requests to the corresponding views.

Parameters
----------
None

Returns
--------
None
"""
from django.urls import path

from appointments.pages.account_views import (
    AccountView,
    UserProfileUpdateView,
    update_profile_picture_view,
)
from appointments.pages.auth_views import (
    AuthView,
    EmployeeAuthView,
    logout_view,
)
from appointments.pages.barber_views import (
    ServicesCreationView,
    ServicesListView,
    DashboardView,
    UpdateStatusView
)
from appointments.pages.scheduling_views import (
    CreateSchedulingView,
    ReadSchedulingView,
    UpdateScheduleView,
    DeleteScheduleView
)
from appointments.views import index_view, our_services_view

app_name = 'appointments'

urlpatterns = [
    # Static views
    path('', index_view, name='index'),
    path('our_services/', our_services_view, name='our_services'),


    # Auth views
    path('authentication/', AuthView.as_view(), name='authentication'),
    path('account/', AccountView.as_view(), name='account'),
    path('logout/', logout_view, name='logout'),
    path('authentication/employee/',
         EmployeeAuthView.as_view(), name='auth_employee'),

    # Update views
    path('account/update/', UserProfileUpdateView.as_view(),
         name='update_profile'),
    path('account/update/profile_picture/', update_profile_picture_view,
         name='update_profile_picture'),

    # Barber views
    path('services/create/', ServicesCreationView.as_view(), name='services'),
    path('services/list/', ServicesListView.as_view(), name='services_list'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('services/update_status/<int:pk>',
         UpdateStatusView.as_view(), name='update_status'),

    # Schedule views
    path('schedules/', ReadSchedulingView.as_view(), name='schedules'),
    path('schedule/create', CreateSchedulingView.as_view(),
         name='create_schedule'),
    path('schedule/update/<int:schedule_id>/', UpdateScheduleView.as_view(),
         name='update_schedule'
         ),
    path('schedule/delete/<int:schedule_id>/', DeleteScheduleView.as_view(),
         name='delete_schedule'
         )
]
