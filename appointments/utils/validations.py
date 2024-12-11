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
                'Defina o "model" e o "field_name" no mixin ou no formulário.'
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
