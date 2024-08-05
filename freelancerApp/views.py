import csv
from datetime import timedelta, timezone
import logging
from django.http import HttpResponse
import pandas as pd
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Freelancer
from .serializers import FreelancerSerializer, FreelancerCreateSerializer

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_freelancer(request):
    try:
        serializer = FreelancerCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error(f"Exception occurred in create_freelancer: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_freelancers(request):
    try:
        freelancers = Freelancer.objects.all()
        serializer = FreelancerSerializer(freelancers, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.error(f"Exception occurred in get_all_freelancers: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def freelancer_detail(request, pk):
    try:
        freelancer = get_object_or_404(Freelancer, pk=pk)
        serializer = FreelancerSerializer(freelancer)
        return Response(serializer.data)
    except Exception as e:
        logging.error(f"Exception occurred in freelancer_detail: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_freelancer(request, pk):
    try:
        freelancer = get_object_or_404(Freelancer, pk=pk)
        serializer = FreelancerCreateSerializer(freelancer, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            freelancer = serializer.save()

            if request.data.get('approved'):
                freelancer.status = 'approved'
                freelancer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error(f"Exception occurred in update_freelancer: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def find_freelancer_by_name(request, name):
    try:
        # name = request.query_params.get('name')
        if not name:
            return Response({'error': 'Name parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        freelancers = Freelancer.objects.filter(user__name__icontains=name)
        serializer = FreelancerSerializer(freelancers, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.error(f"Exception occurred in find_freelancer_by_name: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
def delete_freelancer(request, pk):
    try:
        freelancer = get_object_or_404(Freelancer, pk=pk)
        freelancer.status = 'inactive'
        freelancer.save()
        return Response({'detail': 'Freelancer successfully marked as inactive.'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logging.error(f"Exception occurred in delete_freelancer: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_freelancers_by_address(request, address):
    try:
        # address = request.query_params.get('address')
        if not address:
            return Response({'error': 'Address parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        freelancers = Freelancer.objects.filter(user__address__icontains=address)
        serializer = FreelancerSerializer(freelancers, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.error(f"Exception occurred in get_freelancers_by_address: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_freelancers_by_vehicle_type(request, type):
    try:
        # vehicle_type = request.query_params.get('vehicle_type')
        if not type:
            return Response({'error': 'Vehicle type parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        freelancers = Freelancer.objects.filter(vehicle__type__icontains=type)
        serializer = FreelancerSerializer(freelancers, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.error(f"Exception occurred in get_freelancers_by_vehicle_type: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_total_freelancers(request):
    try:
        total_freelancers = Freelancer.objects.count()
        return Response({'total_freelancers': total_freelancers})
    except Exception as e:
        logging.error(f"Exception occurred in get_total_freelancers: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def freelancer_growth(request):
    try:
        period = request.query_params.get('period')
        if not period:
            return Response({'error': 'Period parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        periods = {
            'day': 1,
            'month': 30,
            'three_months': 90,
            'six_months': 180,
            'year': 365,
            'three_years': 1095,
            'five_years': 1825,
            'ten_years': 3650,
        }

        if period not in periods:
            return Response({'error': 'Invalid period parameter.'}, status=status.HTTP_400_BAD_REQUEST)

        start_date = timezone.now() - timedelta(days=periods[period])
        freelancers = Freelancer.objects.filter(created_date__gte=start_date)
        count = freelancers.count()
        return Response({'count': count})
    except Exception as e:
        logging.error(f"Exception occurred in freelancer_growth: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def download_freelancers_excel(request):
    freelancers = Freelancer.objects.all()
    data = [vars(f) for f in freelancers]
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="freelancer.xlsx"'
    df.to_excel(response, index=False)
    return response

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def download_freelancers_csv(request):
    freelancers = Freelancer.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="freelancer.csv"'
    writer = csv.writer(response)
    writer.writerow(['user_id', 'vehicle_id', 'vehicle_model', 'plate_number', 'status', 'created_date'])
    for freelancer in freelancers:
        writer.writerow([freelancer.user_id, freelancer.vehicle_id, freelancer.vehicle_model, freelancer.plate_number, freelancer.status, freelancer.created_date])
    return response






@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser])
def approve_freelancer(request, pk):
    try:
        freelancer = get_object_or_404(Freelancer, pk=pk)
        freelancer.status = 'approved'
        freelancer.save()
        return Response({'detail': 'Freelancer successfully approved.'}, status=status.HTTP_200_OK)
    except Exception as e:
        logging.error(f"Exception occurred in approve_freelancer: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)