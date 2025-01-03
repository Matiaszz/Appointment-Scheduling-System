from rest_framework import serializers
from .models import BarberService, Scheduling


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


class ScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Scheduling model, providing a formatted representation
    of scheduling data, including client, service, and scheduling details.

    Attributes
    ----------
    service_name : str
        The name of the service associated with the scheduling.
    formatted_date : str
        The formatted date of the scheduling, using a custom date format.

    Methods
    -------
    None
    """

    service_name = serializers.CharField(source='service.service_name')
    formatted_date = serializers.CharField(source='get_formatted_date')

    class Meta:
        model = Scheduling
        fields = [
            'id',  # The unique identifier for the scheduling.
            # The client associated with the scheduling (ForeignKey).
            'client',
            'client_name',  # The name of the client.
            'service_name',  # The name of the service scheduled.
            'formatted_date',  # The formatted date for the scheduling.
            'status',  # The current status of the scheduling.
            'notes',  # Any additional notes for the scheduling.
        ]
