
from django.urls import path
from appointments.views import index_view, our_services_view
from appointments.pages.account_views import (
    AccountView,
    update_profile_picture_view,
    update_user_info
)
from appointments.pages.barber_views import ServicesView
from appointments.pages.auth_views import AuthView, logout_view
app_name = 'appointments'

urlpatterns = [
    # Static views
    path('', index_view, name='index'),
    path('our_services/', our_services_view, name='our_services'),

    # Auth views
    path('authentication/', AuthView.as_view(), name='authentication'),
    path('account/', AccountView.as_view(), name='account'),
    path('logout/', logout_view, name='logout'),

    # Update views
    path('update_profile/', update_user_info,
         name='update_profile'),
    path('update_profile_picture/', update_profile_picture_view,
         name='update_profile_picture'),

    # Barber views
    path('services/create/', ServicesView.as_view(), name='services')

]
