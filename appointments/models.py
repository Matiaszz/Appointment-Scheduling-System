from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
from .utils.validations import validate_positive_price


class CustomUser (AbstractUser):
    """
    CustomUser  extends the default Django user model to include additional
    fields
    and user types.

    Attributes
    ----------
    USER_TYPES : tuple
        A tuple defining the different user types available in the system.

    user_type : CharField
        The type of user (e.g., superuser, manager, employee, client).

    profile_picture : ImageField
        The user's profile picture, allowing specific file types.

    email : EmailField
        The user's email address, which must be unique.

    first_name : CharField
        The user's first name.

    last_name : CharField
        The user's last name.

    phone_number : CharField
        The user's phone number.

    Methods
    -------
    is_superuser_custom()
        Returns True if the user is a superuser.

    is_employee()
        Returns True if the user is an employee.

    is_cliente()
        Returns True if the user is a client.
    """

    USER_TYPES = (
        ('superuser', 'Alto escalão'),
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
        verbose_name='Sobrenome', null=False, blank=False, max_length=70)

    phone_number = models.CharField(
        max_length=11, default='', verbose_name='Número de telefone')

    def is_superuser_custom(self):
        """
        Checks if the user is a superuser.

        Returns
        -------
        bool
            True if the user is a superuser, False otherwise.
        """
        return self.user_type == 'superuser'

    def is_employee(self):
        """
        Checks if the user is an employee.

        Returns
        -------
        bool
            True if the user is an employee, False otherwise.
        """
        return self.user_type == 'employee'

    def is_cliente(self):
        """
        Checks if the user is a client.

        Returns
        -------
        bool
            True if the user is a client, False otherwise.
        """
        return self.user_type == 'client'


class BarberService(models.Model):
    """
    BarberService represents a service offered by the barber shop.

    Attributes
    ----------
    SERVICE_TYPES : tuple
        A tuple defining the different types of services available.

    service_name : CharField
        The name of the service.

    price : DecimalField
        The price of the service, validated to be a positive value.

    service_type : CharField
        The type of service (e.g., hair, eyebrow, beard).

    description : TextField
        A description of the service.

    image : ImageField
        An image representing the service, allowing specific file types.

    is_active : BooleanField
        Indicates whether the service is currently active.

    duration : PositiveIntegerField
        The duration of the service in minutes.

    Methods
    -------
    __str__()
        Returns a string representation of the service, including its name and
        price.
    """

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
        """
        Returns a string representation of the service, including its name and
        price.

        Returns
        -------
        str
            A string in the format 'service_name - R$ price'.
        """
        return f'{self.service_name} - R$ {self.price}'
