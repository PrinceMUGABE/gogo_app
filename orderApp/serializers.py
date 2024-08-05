from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_status_display(self, obj):
        return "available" if obj.status else "unavailable"



# serializers.py
from rest_framework import serializers
from .models import Order
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
