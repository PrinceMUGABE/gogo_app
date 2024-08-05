# trackingApp/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from .models import Tracking
from .serializers import TrackingSerializer

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_tracking(request):
    serializer = TrackingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_tracking_by_id(request, id):
    tracking = get_object_or_404(Tracking, id=id)
    serializer = TrackingSerializer(tracking)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_all_tracking(request):
    trackings = Tracking.objects.all()
    serializer = TrackingSerializer(trackings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_tracking_by_longitude(request, longitude):
    trackings = Tracking.objects.filter(longitude=longitude)
    serializer = TrackingSerializer(trackings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_tracking_by_latitude(request, latitude):
    trackings = Tracking.objects.filter(latitude=latitude)
    serializer = TrackingSerializer(trackings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_tracking_by_car(request, car_id):
    trackings = Tracking.objects.filter(car_id=car_id)
    serializer = TrackingSerializer(trackings, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_tracking_by_id(request, id):
    tracking = get_object_or_404(Tracking, id=id)
    serializer = TrackingSerializer(tracking, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_tracking_by_id(request, id):
    tracking = get_object_or_404(Tracking, id=id)
    tracking.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
