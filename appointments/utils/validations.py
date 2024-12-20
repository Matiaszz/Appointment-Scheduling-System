from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.forms import forms


def validate_positive_price(value):
    if value <= 0:
        raise ValidationError('O preço deve ser um valor positivo.')


class UniqueFieldValidationMixin:
    model = None
    field_name = None

    def clean_unique_field(self):
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
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_client():
            raise PermissionDenied(
                'Você não tem permissão para acessar esta página.')
        return super().dispatch(request, *args, **kwargs)  # type: ignore


class OnlyManagerOrSuperuserMixin:
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated
                or not request.user.is_superuser_custom()
                or not request.user.is_manager()
                ):
            raise PermissionDenied(
                'Você não tem permissão para acessar esta página.')

        return super().dispatch(request, *args, **kwargs)  # type: ignore


class OnlySuperuserMixin:
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated
                or not request.user.is_superuser_custom()
                ):
            raise PermissionDenied(
                'Você não tem permissão para acessar esta página.')

        return super().dispatch(request, *args, **kwargs)  # type: ignore
