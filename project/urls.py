"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.shortcuts import render
from django.conf.urls import handler404, handler403
from appointments.pages.barber_views import ServiceViewSet
from appointments.pages.scheduling_views import ScheduleViewSet
from appointments.views import custom_403_view, custom_404_view
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler403 = custom_403_view
handler404 = custom_404_view


router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')
router.register(r'schedules', ScheduleViewSet, basename='schedules')

urlpatterns = [
    path('', include('appointments.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('contact/', lambda request: render(request,
         'contact_us.html'), name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
