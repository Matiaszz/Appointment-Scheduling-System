from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.forms import forms


def validate_positive_price(value):
    """
    Validator function to ensure that a price is positive.

    Parameters
    ----------
    value : float
        The price value to be validated.

    Raises
    ------
    ValidationError
        If the price is less than or equal to zero, a ValidationError is
        raised.
    """
    if value <= 0:
        raise ValidationError('O preço deve ser um valor positivo.')


class UniqueFieldValidationMixin:
    """
    A mixin that ensures a field value is unique within a given model.

    This mixin is used to validate that a field value (e.g., email or username)
    does not already exist in the model.

    Attributes
    ----------
    model : Model
        The model in which the field is being validated.
    field_name : str
        The field name to be validated for uniqueness.

    Methods
    -------
    clean_unique_field()
        Validates if the value of the specified field is unique in the model.
    """

    model = None
    field_name = None

    def clean_unique_field(self):
        """
        Validates that the value of a specified field is unique within the
        model.

        Returns
        -------
        value : Any
            The value of the field, if it is unique.

        Raises
        ------
        NotImplementedError
            If the "model" or "field_name" attributes are not defined.
        forms.ValidationError
            If the field value is not unique.
        """
        if not self.model or not self.field_name:
            raise NotImplementedError(
                'Define de "model" and '
                '"field_name" in the form or in the mixin.'
            )

        value = self.cleaned_data.get(self.field_name)  # type: ignore
        if not value:
            return value

        queryset = self.model.objects.filter(**{self.field_name: value})
        if self.instance.pk:  # type: ignore
            queryset = queryset.exclude(pk=self.instance.pk)  # type: ignore

        if queryset.exists():
            raise forms.ValidationError(
                f'Este {self.field_name} já está cadastrado.'
            )
        return value


class OnlyStaffMixin:
    """
    Mixin that restricts access to a view to only authenticated users who are
    staff members.

    Methods
    -------
    dispatch(request, *args, **kwargs)
        Checks if the user is authenticated and has staff permissions.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Restricts access to staff users only.

        Parameters
        ----------
        request : HttpRequest
            The request object containing metadata about the request.

        *args, **kwargs :
            Additional arguments that may be passed to the view.

        Returns
        -------
        HttpResponse
            The response for the view if the user is authorized.

        Raises
        ------
        PermissionDenied
            If the user is not authenticated or is a client user.
        """
        if not request.user.is_authenticated or request.user.is_client():
            raise PermissionDenied(
                'Você não tem permissão para acessar esta página.')
        return super().dispatch(request, *args, **kwargs)  # type: ignore


class OnlyManagerOrSuperuserMixin:
    """
    Mixin that restricts access to a view to only authenticated users who are
    either
    managers or superusers.

    Methods
    -------
    dispatch(request, *args, **kwargs)
        Checks if the user is authenticated and has manager or superuser
        permissions.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Restricts access to managers or superusers only.

        Parameters
        ----------
        request : HttpRequest
            The request object containing metadata about the request.

        *args, **kwargs :
            Additional arguments that may be passed to the view.

        Returns
        -------
        HttpResponse
            The response for the view if the user is authorized.

        Raises
        ------
        PermissionDenied
            If the user is not authenticated, not a manager, or not a
            superuser.
        """
        if not (request.user.is_authenticated
                or not request.user.is_superuser_custom()
                or not request.user.is_manager()
                ):
            raise PermissionDenied(
                'Você não tem permissão para acessar esta página.')

        return super().dispatch(request, *args, **kwargs)  # type: ignore


class OnlySuperuserMixin:
    """
    Mixin that restricts access to a view to only authenticated superusers.

    Methods
    -------
    dispatch(request, *args, **kwargs)
        Checks if the user is authenticated and has superuser permissions.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Restricts access to superusers only.

        Parameters
        ----------
        request : HttpRequest
            The request object containing metadata about the request.

        *args, **kwargs :
            Additional arguments that may be passed to the view.

        Returns
        -------
        HttpResponse
            The response for the view if the user is authorized.

        Raises
        ------
        PermissionDenied
            If the user is not authenticated or not a superuser.
        """
        if not (request.user.is_authenticated
                or not request.user.is_superuser_custom()
                ):
            raise PermissionDenied(
                'Você não tem permissão para acessar esta página.')

        return super().dispatch(request, *args, **kwargs)  # type: ignore
