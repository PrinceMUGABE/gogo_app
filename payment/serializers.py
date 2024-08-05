from rest_framework import serializers
from .models import Payment, Order
from userApp.models import CustomUser

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        order_data = validated_data.pop('order')
        order = Order.objects.create(**order_data)
        payment = Payment.objects.create(order=order, **validated_data)
        return payment

    def update(self, instance, validated_data):
        order_data = validated_data.pop('order')
        order = instance.order

        instance.ref = validated_data.get('ref', instance.ref)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.provider = validated_data.get('provider', instance.provider)
        instance.status = validated_data.get('status', instance.status)
        instance.kind = validated_data.get('kind', instance.kind)
        instance.save()

        order.order_name = order_data.get('order_name', order.order_name)
        order.origin = order_data.get('origin', order.origin)
        order.destination = order_data.get('destination', order.destination)
        order.total_price = order_data.get('total_price', order.total_price)
        order.vehicle_type = order_data.get('vehicle_type', order.vehicle_type)
        order.type = order_data.get('type', order.type)
        order.payment_status = order_data.get('payment_status', order.payment_status)
        order.save()

        return instance
