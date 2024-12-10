from django.core.exceptions import ValidationError


def validate_positive_price(value):
    if value <= 0:
        raise ValidationError('O preço deve ser um valor positivo.')
