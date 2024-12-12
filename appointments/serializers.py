from rest_framework import serializers, viewsets
from .models import BarberService


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarberService
        fields = '__all__'
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
