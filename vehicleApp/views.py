from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

from userApp.models import CustomUser
from .models import Vehicle
from .serializers import VehicleSerializer, VehicleCreateSerializer
from django.http import HttpResponse
import csv
import pandas as pd
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


# Import logging and configure basic settings
import logging
logging.basicConfig(filename='vehicle_app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Vehicle
import logging



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vehicle(request):
    try:
        # Log the user information
        logging.info(f"User attempting to create vehicle: {request.user} (ID: {request.user.id})")

        # Check if the logged-in user is an admin
        if request.user.role != 'admin':
            logging.warning(f"User {request.user.email} is not an admin and cannot create vehicles.")
            return Response({'error': 'Only admin users can create vehicles.'}, status=status.HTTP_403_FORBIDDEN)

        # Extract data from the request
        data = request.data
        vehicle_type = data.get('type')
        total_weight_to_carry = data.get('total_weight_to_carry')
        price_per_km = data.get('price_per_km')
        
        # Validate data
        if not vehicle_type or not total_weight_to_carry or not price_per_km:
            logging.error("Missing required fields in create_vehicle request data.")
            return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate vehicle type
        if Vehicle.objects.filter(type=vehicle_type).exists():
            logging.warning(f"Vehicle with type '{vehicle_type}' already exists.")
            return Response({'error': f"Vehicle with type '{vehicle_type}' already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create vehicle instance
        vehicle = Vehicle(
            type=vehicle_type,
            total_weight_to_carry=total_weight_to_carry,
            price_per_km=price_per_km,
            created_by=request.user  # Assign the current logged-in user
        )
        vehicle.save()

        # Return the created vehicle data
        vehicle_data = {
            'id': vehicle.id,
            'type': vehicle.type,
            'total_weight_to_carry': vehicle.total_weight_to_carry,
            'price_per_km': vehicle.price_per_km,
            'created_date': vehicle.created_date,
            'created_by': vehicle.created_by.email  # Include the creator's email in the response
        }

        return Response(vehicle_data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logging.error(f"Exception occurred in create_vehicle: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def vehicle_detail(request, pk):
    try:
        vehicle = get_object_or_404(Vehicle, pk=pk)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)
    except Vehicle.DoesNotExist:
        logging.error(f"Vehicle with id {pk} does not exist")
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logging.error(f"Exception occurred in vehicle_detail: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def vehicle_detail(request, pk):
    try:
        vehicle = get_object_or_404(Vehicle, pk=pk)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)
    except Vehicle.DoesNotExist:
        logging.error(f"Vehicle with id {pk} does not exist")
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logging.error(f"Exception occurred in vehicle_detail: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_vehicle(request, pk):
    try:
        vehicle = get_object_or_404(Vehicle, pk=pk)
        serializer = VehicleCreateSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            logging.error(f"Invalid data received in update_vehicle: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Vehicle.DoesNotExist:
        logging.error(f"Vehicle with id {pk} does not exist")
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logging.error(f"Exception occurred in update_vehicle: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_vehicle(request, pk):
    try:
        vehicle = get_object_or_404(Vehicle, pk=pk)
        vehicle.delete()
        return Response({'detail': 'Vehicle successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
    except Vehicle.DoesNotExist:
        logging.error(f"Vehicle with id {pk} does not exist")
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logging.error(f"Exception occurred in delete_vehicle: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_vehicles(request):
    try:
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.error(f"Exception occurred in list_vehicles: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_vehicle_by_type(request):
    try:
        vehicle_type = request.query_params.get('type')
        if not vehicle_type:
            return Response({'error': 'Type parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        vehicles = Vehicle.objects.filter(type=vehicle_type)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.error(f"Exception occurred in search_vehicle_by_type: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([IsAdminUser])
def total_vehicles(request):
    try:
        total_vehicles = Vehicle.objects.count()
        return Response({'total_vehicles': total_vehicles})
    except Exception as e:
        logging.error(f"Exception occurred in total_vehicles: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def vehicles_by_total_weight(request):
    try:
        total_weight = request.query_params.get('total_weight')
        if not total_weight:
            return Response({'error': 'Total weight parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        vehicles = Vehicle.objects.filter(total_weight_to_carry=total_weight)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.error(f"Exception occurred in vehicles_by_total_weight: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def vehicles_by_price_per_km(request):
    try:
        price_per_km = request.query_params.get('price_per_km')
        if not price_per_km:
            return Response({'error': 'Price per km parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        vehicles = Vehicle.objects.filter(price_per_km=price_per_km)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.error(f"Exception occurred in vehicles_by_price_per_km: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def vehicle_stats(request):
    try:
        now = timezone.now()
        stats = {
            'daily': Vehicle.objects.filter(created_date__gte=now - timedelta(days=1)).count(),
            'weekly': Vehicle.objects.filter(created_date__gte=now - timedelta(weeks=1)).count(),
            'monthly': Vehicle.objects.filter(created_date__gte=now - timedelta(days=30)).count(),
            'three_months': Vehicle.objects.filter(created_date__gte=now - timedelta(days=90)).count(),
            'six_months': Vehicle.objects.filter(created_date__gte=now - timedelta(days=180)).count(),
            'yearly': Vehicle.objects.filter(created_date__gte=now - timedelta(days=365)).count(),
            'three_years': Vehicle.objects.filter(created_date__gte=now - timedelta(days=3*365)).count(),
            'five_years': Vehicle.objects.filter(created_date__gte=now - timedelta(days=5*365)).count(),
            'ten_years': Vehicle.objects.filter(created_date__gte=now - timedelta(days=10*365)).count(),
        }
        return Response(stats)
    except Exception as e:
        logging.error(f"Exception occurred in vehicle_stats: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_vehicles(request, format=None):
    try:
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)

        # Create CSV response
        csv_file = HttpResponse(content_type='text/csv')
        csv_file['Content-Disposition'] = 'attachment; filename="vehicles.csv"'
        writer = csv.writer(csv_file)
        writer.writerow(['ID', 'Type', 'Total Weight to Carry', 'Created By', 'Price per KM', 'Created Date'])
        for vehicle in serializer.data:
            writer.writerow([vehicle['id'], vehicle['type'], vehicle['total_weight_to_carry'],
                             vehicle['created_by'], vehicle['price_per_km'], vehicle['created_date']])

        # Create Excel response
        excel_file = HttpResponse(content_type='application/vnd.ms-excel')
        excel_file['Content-Disposition'] = 'attachment; filename="vehicles.xlsx"'
        df = pd.DataFrame(serializer.data)
        df.to_excel(excel_file, index=False)

        return Response({
            'csv': csv_file,
            'excel': excel_file,
        })
    except Exception as e:
        logging.error(f"Exception occurred in download_vehicles: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
