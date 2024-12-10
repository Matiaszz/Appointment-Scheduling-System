from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('superuser', 'Superuser'),
        ('employee', 'Funcionário'),
        ('client', 'Cliente'),
    )
    user_type = models.CharField(
        max_length=20, choices=USER_TYPES, default='client')

    profile_picture = models.ImageField(
        upload_to='profile_pictures/%Y/%m',
        default='profile_pictures/default.jpg',
        blank=True, null=True,
        verbose_name='Foto de perfil',
        validators=[FileExtensionValidator(allowed_extensions=[
            'jpg', 'jpeg', 'png'])]
    )
    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=11, default='')

    def is_superuser_custom(self):
        return self.user_type == 'superuser'

    def is_employee(self):
        return self.user_type == 'employee'

    def is_cliente(self):
        return self.user_type == 'client'
