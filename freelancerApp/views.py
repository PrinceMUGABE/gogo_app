

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Freelancer
from .serializers import FreelancerSerializer, FreelancerCreateSerializer

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_freelancer(request):
    serializer = FreelancerCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_freelancers(request):
    freelancers = Freelancer.objects.all()
    serializer = FreelancerSerializer(freelancers, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_freelancer(request, pk):
    freelancer = get_object_or_404(Freelancer, pk=pk)
    serializer = FreelancerCreateSerializer(freelancer, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser])
def approve_freelancer(request, pk):
    freelancer = get_object_or_404(Freelancer, pk=pk)
    freelancer.status = 'approved'
    freelancer.save()
    return Response({'detail': 'Freelancer successfully approved.'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser])
def deny_freelancer(request, pk):
    freelancer = get_object_or_404(Freelancer, pk=pk)
    freelancer.status = 'denied'
    freelancer.save()
    return Response({'detail': 'Freelancer successfully denied.'}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_freelancer_by_id(request, pk):
    freelancer = get_object_or_404(Freelancer, pk=pk)
    serializer = FreelancerSerializer(freelancer)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def view_freelancer_details(request, pk):
    freelancer = get_object_or_404(Freelancer, pk=pk)

    user = freelancer.user
    vehicle = freelancer.vehicle
    company = freelancer.company

    details = {
        "freelancer_id": freelancer.id,
        "vehicle_type": vehicle.type,  # Changed to vehicle.type
        "plate_number": freelancer.plate_number,
        "vehicle_model": freelancer.vehicle_model,
        "national_id_card": freelancer.national_id_card.url if freelancer.national_id_card else None,
        "driving_license": freelancer.driving_license.url if freelancer.driving_license else None,
        "status": freelancer.status,
        "created_date": freelancer.created_date,
        "user": {
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
        },
        "company": {
            "id": company.id,
            "name": company.name,
            "location": company.location,
            "status": company.status,
            # "rdb_certificate": company.rdb_certificate,
            # "iso_certificate": company.iso_certificate,
            # Add other company details if needed
        },
        "vehicle": {
            "id": vehicle.id,
            "type": vehicle.type,
            # Add other vehicle details if needed
        },
    }
    return Response(details)


@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
def delete_freelancer(request, pk):
    try:
        freelancer = get_object_or_404(Freelancer, pk=pk)
        freelancer.delete()  # Permanently delete the freelancer
        return Response({'detail': 'Freelancer successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logging.error(f"Exception occurred in delete_freelancer: {str(e)}")
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

