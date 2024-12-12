
from django.urls import path
from appointments.views import index_view, our_services_view
from appointments.pages.account_views import (
    AccountView,
    update_profile_picture_view,
    UserProfileUpdateView
)
from appointments.pages.barber_views import ServicesView, ServicesListView
from appointments.pages.auth_views import AuthView, logout_view, EmployeeAuthView
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
    path('services/create/', ServicesView.as_view(), name='services'),
    path('services/list/', ServicesListView.as_view(), name='services_list'),

]
