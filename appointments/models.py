from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
from .utils.validations import validate_positive_price


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('superuser', 'Superuser'),
        ('manager', 'Gerente'),
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

    first_name = models.CharField(
        verbose_name='Nome', null=False, blank=False, max_length=70)

    last_name = models.CharField(
        verbose_name='Nome', null=False, blank=False, max_length=70)

    phone_number = models.CharField(
        max_length=11, default='', verbose_name='Número de telefone')

    def is_superuser_custom(self):
        return self.user_type == 'superuser'

    def is_employee(self):
        return self.user_type == 'employee'

    def is_cliente(self):
        return self.user_type == 'client'


class BarberService(models.Model):
    SERVICE_TYPES = (
        ('hair', 'Cabelo'),
        ('eyebrow', 'Sobrancelha'),
        ('beard', 'Barba'),
        ('kids_haircut', 'Corte infantil'),
        ('hair_treatment', 'Tratamento capilar'),
        ('custom', 'Personalizado'),
    )

    service_name = models.CharField(
        max_length=50, verbose_name='Nome do serviço')

    price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[validate_positive_price],
        verbose_name='Preço')

    service_type = models.CharField(
        max_length=30, choices=SERVICE_TYPES, default='hair',
        verbose_name='Tipo de serviço')

    description = models.TextField(
        blank=True, verbose_name='Descrição do serviço')

    image = models.ImageField(
        upload_to='services/%Y/%m', blank=True, null=True,
        verbose_name='Imagem do serviço',
        validators=[FileExtensionValidator(allowed_extensions=[
            'jpg', 'jpeg', 'png'])],
        default='services/default.jpg',
    )

    is_active = models.BooleanField(
        default=True, verbose_name='Serviço Ativo')

    duration = models.PositiveIntegerField(
        verbose_name='Duração (minutos)')

    def __str__(self):
        return f'{self.service_name} - R$ {self.price}'
