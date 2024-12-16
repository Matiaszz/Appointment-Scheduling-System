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
from appointments.pages.barber_views import ServiceViewSet
from appointments.pages.scheduling_views import ScheduleViewSet
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')
router.register(r'schedules', ScheduleViewSet, basename='schedules')

urlpatterns = [
    path('', include('appointments.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
