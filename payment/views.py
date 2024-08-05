from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Payment, Order
from .serializers import PaymentSerializer, OrderSerializer
from userApp.models import CustomUser

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_all_payments(request):
    payments = Payment.objects.all()
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment_by_id(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
    except Payment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PaymentSerializer(payment)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment_by_order(request, order_id):
    try:
        payment = Payment.objects.get(order_id=order_id)
    except Payment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PaymentSerializer(payment)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payments_by_status(request, status):
    payments = Payment.objects.filter(status=status)
    if not payments.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payments_by_provider(request, provider):
    payments = Payment.objects.filter(provider=provider)
    if not payments.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payments_by_kind(request, kind):
    payments = Payment.objects.filter(kind=kind)
    if not payments.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_payment(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
    except Payment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PaymentSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_payment(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
    except Payment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    payment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders_by_user(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    orders = user.orders.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
