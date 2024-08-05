from rest_framework import serializers
from .models import DiscountOrder

class DiscountOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountOrder
        fields = '__all__'
