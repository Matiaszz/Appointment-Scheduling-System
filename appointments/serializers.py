from rest_framework import serializers
from .models import BarberService


class ServiceSerializer(serializers.ModelSerializer):
    """
    ServiceSerializer serializes the BarberService model for use in API
    responses and requests.

    This serializer converts the BarberService model instances into JSON
    format and validates incoming data for creating or updating services.


    Attributes
    ----------
    price : DecimalField
        A field that represents the price of the service, with a maximum of 10
        digits and 2 decimal places.

    Meta
    ----
    model : BarberService
        The model that this serializer is based on.

    fields : list
        A list of fields to be included in the serialized output. Using
        '__all__' includes all fields from the model.
    """

    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = BarberService
        fields = '__all__'
