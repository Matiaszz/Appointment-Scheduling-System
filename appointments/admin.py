from django.contrib import admin
from .models import CustomUser, BarberService


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(BarberService)
class BarberServiceAdmin(admin.ModelAdmin):
    pass
