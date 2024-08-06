from datetime import timezone
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now, timedelta
from django.db.models import Count
from .serializers import CustomUserSerializer, UpdateUserSerializer
from userApp.models import CustomUser
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        send_mail(
            'Welcome to GoGo_App',
            'Hello {},\n\nYour account has been created successfully. Welcome to GoGo_App!'.format(user.name),
            'your-email@example.com',
            [user.email],
            fail_silently=False,
        )
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    else:
        logger.error("Serializer errors: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from userApp.models import CustomUser
from userApp.serializers import CustomUserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = CustomUser.objects.get(email=email)
        if not check_password(password, user.password):
            return Response({'error': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)

        user_data = CustomUserSerializer(user).data
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': user_data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_user_by_id(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        user_data = CustomUserSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_phone(request, phone):
    try:
        user = CustomUser.objects.get(phone=phone)
        user_data = CustomUserSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_email(request, email):
    try:
        user = CustomUser.objects.get(email=email)
        user_data = CustomUserSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_all_users(request):
    users = CustomUser.objects.all()
    users_data = CustomUserSerializer(users, many=True).data
    return Response(users_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_by_role(request, role):
    users = CustomUser.objects.filter(role=role)
    users_data = CustomUserSerializer(users, many=True).data
    return Response(users_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_by_address(request, address):
    users = CustomUser.objects.filter(address__icontains=address)
    users_data = CustomUserSerializer(users, many=True).data
    return Response(users_data, status=status.HTTP_200_OK)




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        user.delete()
        return Response({'message': 'User deleted successfully.'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_total_users(request):
    total_users = CustomUser.objects.count()
    return Response({'total_users': total_users}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_growth_statistics(request):
    now = timezone.now()
    intervals = {
        'daily': now - timedelta(days=1),
        'weekly': now - timedelta(weeks=1),
        'monthly': now - timedelta(days=30),
        'three_months': now - timedelta(days=90),
        'six_months': now - timedelta(days=180),
        'yearly': now - timedelta(days=365),
        'three_years': now - timedelta(days=3*365),
        'five_years': now - timedelta(days=5*365),
        'ten_years': now - timedelta(days=10*365),
    }

    growth_data = {}
    for key, value in intervals.items():
        count = CustomUser.objects.filter(created_date__gte=value).count()
        growth_data[key] = count

    return Response(growth_data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    email = request.data.get('email')
    new_password = request.data.get('new_password')

    try:
        user = CustomUser.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)





@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, id):
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UpdateUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User details updated successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({'message': 'Logout successful.'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)