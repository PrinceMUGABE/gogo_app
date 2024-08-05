# orderApplicationApp/serializers.py
from rest_framework import serializers
from .models import OrderApplication

class OrderApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderApplication
        fields = '__all__'
