from django.contrib import admin
from .models import CustomUser, BarberService, Scheduling


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(BarberService)
class BarberServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Scheduling)
class SchedulingAdmin(admin.ModelAdmin):
    pass
