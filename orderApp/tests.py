<<<<<<< HEAD
from django.test import TestCase

# Create your tests here.
=======
# orders/serializers.py
from rest_framework import serializers
from .models import Order, Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

# orders/serializers.py
class OrderSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_status_display(self, obj):
        return "available" if obj.status else "unavailable"
>>>>>>> 369378f (first commit)
