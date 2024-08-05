import io
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from .models import Order, Vehicle
from .serializers import OrderSerializer
from paypack.client import HttpClient
from paypack.transactions import Transaction
from . serializers import PaymentSerializer

client_id = "85d99eae-4dc4-11ef-9da3-deade826d28d"
client_secret = "c55cd366ead0e6d67d8eaef055a3a441da39a3ee5e6b4b0d3255bfef95601890afd80709"

# Initialize the Paypack client
paypack_client = HttpClient(client_id=client_id, client_secret=client_secret)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_order(request):
    try:
        data = request.data.copy()
        data['created_by'] = request.user.id

        # Get vehicle details
        vehicle = get_object_or_404(Vehicle, id=data.get('vehicle_type'))
        
        # Convert distance to Decimal
        distance = Decimal(data.get('distance'))
        
        # Calculate the total price based on distance and vehicle price per km
        total_price = (vehicle.price_per_km * distance).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Ensure total price meets the minimum amount required by Paypack
        min_amount = Decimal('100.00')
        if total_price < min_amount:
            total_price = min_amount

        data['total_price'] = total_price

        # Initialize the serializer with the request data
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            # Ensure phone_number is passed in the request data
            phone_number = data.get('phone_number')
            if not phone_number:
                return Response({'detail': 'Phone number is required for payment.'}, status=status.HTTP_400_BAD_REQUEST)

            # Attempt to process the payment
            cashin_response = Transaction().cashin(amount=total_price, phone_number=phone_number)

            # Log the cashin response for debugging purposes
            print(cashin_response)

            # Update payment status based on Paypack response
            payment_status = cashin_response.get('status', 'pending')
            data['payment_status'] = payment_status

            # Save the order
            order = serializer.save()

            # Create a payment record
            payment_data = {
                'order': order.id,
                'ref': cashin_response.get('ref', ''),
                'status': payment_status,
                'amount': total_price,
                'provider': cashin_response.get('provider', ''),
                'kind': cashin_response.get('kind', '')
            }
            payment_serializer = PaymentSerializer(data=payment_data)
            if payment_serializer.is_valid():
                payment_serializer.save()
            else:
                # Handle payment creation error
                return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def display_all_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_order_by_id(request, pk):
    order = get_object_or_404(Order, pk=pk)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_order_by_name(request, name):
    orders = Order.objects.filter(order_name__icontains=name)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_orders_by_vehicle_type(request, vehicle_type_id):
    orders = Order.objects.filter(vehicle_type_id=vehicle_type_id)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_order(request, pk):
    try:
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_order(request, pk):
    try:
        order = get_object_or_404(Order, pk=pk)
        data = request.data.copy()
        data['created_by'] = order.created_by.id  # Ensure created_by remains unchanged
        serializer = OrderSerializer(order, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_orders_pdf(request):
    orders = Order.objects.all()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    p.drawString(100, height - 50, "Orders List")
    
    y = height - 100
    for order in orders:
        p.drawString(100, y, f"Order: {order.order_name}, Origin: {order.origin}, Destination: {order.destination}, Total Price: {order.total_price}")
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_orders.pdf"'
    return response


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_orders_excel(request):
    orders = Order.objects.all()
    order_data = [
        {
            "Order Name": order.order_name,
            "Origin": order.origin,
            "Destination": order.destination,
            "Total Price": order.total_price,
            "Vehicle Type": order.vehicle_type.type,
            "Created Date": order.created_date,
        }
        for order in orders
    ]
    df = pd.DataFrame(order_data)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Orders')
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="all_orders.xlsx"'
    return response


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_orders_csv(request):
    orders = Order.objects.all()
    order_data = [
        {
            "Order Name": order.order_name,
            "Origin": order.origin,
            "Destination": order.destination,
            "Total Price": order.total_price,
            "Vehicle Type": order.vehicle_type.type,
            "Created Date": order.created_date,
        }
        for order in orders
    ]
    df = pd.DataFrame(order_data)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_orders.csv"'
    return response
