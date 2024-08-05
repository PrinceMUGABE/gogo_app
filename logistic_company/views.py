# views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_company(request):
    user = request.user
    data = request.data.copy()
    data['user'] = user.id
    serializer = CompanySerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_all_companies(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_company_by_id(request, pk):
    try:
        company = Company.objects.get(pk=pk)
    except Company.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CompanySerializer(company)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_company_by_name(request, name):
    try:
        company = Company.objects.get(name=name)
    except Company.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CompanySerializer(company)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_companies_by_location(request, location):
    companies = Company.objects.filter(location=location)
    if not companies:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_company(request, pk):
    try:
        company = Company.objects.get(pk=pk)
    except Company.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if company.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = CompanySerializer(company, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_company(request, pk):
    try:
        company = Company.objects.get(pk=pk)
    except Company.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if company.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    company.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_companies_by_status(request, status):
    companies = Company.objects.filter(status=status)
    if not companies:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)
