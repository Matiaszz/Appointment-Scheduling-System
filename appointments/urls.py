
from django.urls import path
from appointments.views import (index_view, AuthView, AccountView,
                                logout_view, update_profile_picture,
                                update_user_info)

app_name = 'appointments'

urlpatterns = [
    path('', index_view, name='index'),
    path('authentication/', AuthView.as_view(), name='authentication'),
    path('account/', AccountView.as_view(), name='account'),
    path('update_profile/', update_user_info,
         name='update_profile'),
    path('update_profile_picture/', update_profile_picture,
         name='update_profile_picture'),
    path('logout/', logout_view, name='logout')
]
