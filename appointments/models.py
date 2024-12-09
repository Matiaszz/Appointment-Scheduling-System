from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('superuser', 'Superuser'),
        ('employee', 'Funcionário'),
        ('client', 'Cliente'),
    )
    user_type = models.CharField(
        max_length=20, choices=USER_TYPES, default='client')

    def is_superuser_custom(self):
        return self.user_type == 'superuser'

    def is_employee(self):
        return self.user_type == 'employee'

    def is_cliente(self):
        return self.user_type == 'client'
