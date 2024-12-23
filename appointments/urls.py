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
    DeactivateAccountView,
    update_profile_picture_view,
)
from appointments.pages.auth_views import (
    AuthView,
    EmployeeAuthView,
    ManagerAuthView,
    CEOAuthView,
    logout_view,
)
from appointments.pages.barber_views import (
    CreateServicesView,
    ListServicesView,
    UpdateServicesView,
    DashboardView,
    GetEmployeesView,
    UpdateStatusView
)
from appointments.pages.scheduling_views import (
    CreateSchedulingView,
    ListSchedulesView,
    DetailScheduleView,
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
    path('logout/', logout_view, name='logout'),
    path('authentication/employee/',
         EmployeeAuthView.as_view(), name='auth_employee'),
    path('authentication/manager/',
         ManagerAuthView.as_view(), name='auth_manager'),
    path('authentication/ceo/', CEOAuthView.as_view(), name='auth_ceo'),

    # Account views
    path('account/', AccountView.as_view(), name='account'),
    path('account/<int:pk>/', AccountView.as_view(), name='account_with_id'),
    path('account/update/', UserProfileUpdateView.as_view(),
         name='update_profile'),
    path('account/update/profile_picture/', update_profile_picture_view,
         name='update_profile_picture'),
    path('account/<int:pk>/deactivate/', DeactivateAccountView.as_view(),
         name='deactivate_account'),

    # Barber views
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/employees/', GetEmployeesView.as_view(),
         name='get_employees'),
    path('services/create/', CreateServicesView.as_view(), name='services'),
    path('services/list/', ListServicesView.as_view(), name='services_list'),
    path('services/update/<int:pk>/', UpdateServicesView.as_view(),
         name='update_service'),
    path('services/update_status/<int:pk>',
         UpdateStatusView.as_view(), name='update_status'),

    # Schedule views
    path('schedules/', ListSchedulesView.as_view(), name='schedules'),
    path('schedule/<int:schedule_id>/',
         DetailScheduleView.as_view(), name='detail_schedule'),
    path('schedule/create', CreateSchedulingView.as_view(),
         name='create_schedule'),
    path('schedule/update/<int:schedule_id>/', UpdateScheduleView.as_view(),
         name='update_schedule'
         ),
    path('schedule/delete/<int:schedule_id>/', DeleteScheduleView.as_view(),
         name='delete_schedule'
         )
]
