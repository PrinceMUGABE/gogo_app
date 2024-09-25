<<<<<<< HEAD
from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
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
>>>>>>> 369378f (first commit)
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_status_display(self, obj):
        return "available" if obj.status else "unavailable"
<<<<<<< HEAD

    def validate(self, data):
        # Validate that order_name has at least 3 characters
        if len(data.get('order_name', '')) < 3:
            raise serializers.ValidationError({"order_name": "Order name must be at least 3 characters long."})

        # Ensure total_price is a positive number
        total_price = data.get('total_price')
        if total_price is not None and total_price <= 0:
            raise serializers.ValidationError({"total_price": "Total price must be greater than zero."})

        return data



# serializers.py
from rest_framework import serializers
from .models import Order
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
=======
>>>>>>> 369378f (first commit)
