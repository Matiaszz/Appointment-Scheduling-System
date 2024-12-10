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


class BarberService(models.Model):
    SERVICE_TYPES = (
        ('hair', 'Cabelo'),
        ('beard', 'Barba'),
        ('kids_haircut', 'Corte infantil'),
        ('hair_treatment', 'Tratamento capilar'),
        ('custom', 'Personalizado'),
    )

    PAYMENT_STATUS_TYPES = (
        ('paid', 'Pago'),
        ('pending', 'Pendente'),
        ('canceled', 'Cancelado'),

    )
    service_name = models.CharField(
        max_length=50, verbose_name='Nome do serviço')

    price = models.DecimalField(max_digits=6, decimal_places=2)

    service_type = models.CharField(
        max_length=30, choices=SERVICE_TYPES, default='custom')

    payment_status_type = models.CharField(
        max_length=30, choices=PAYMENT_STATUS_TYPES, default='pending')

    def __str__(self):
        return f"{self.service_name} - R$ {self.price}"
