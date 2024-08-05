# serializers.py
from rest_framework import serializers
from .models import Company
from userApp.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'phone', 'role', 'address']

class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Company
        fields = '__all__'
