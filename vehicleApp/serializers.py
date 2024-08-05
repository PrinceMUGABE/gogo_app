from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class VehicleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['type', 'total_weight_to_carry', 'price_per_km']
