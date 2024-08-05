from rest_framework import serializers
from .models import CustomUser
import re

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id' ,'email', 'name', 'phone', 'password', 'confirm_password', 'role', 'address']

    def validate_phone(self, value):
        if not re.match(r'^(078|072|073|079)\d{7}$', value):
            raise serializers.ValidationError("Phone number must be 10 digits and start with 078, 072, 073, or 079.")
        return value

    def validate_email(self, value):
        if re.match(r'^[\d\W]', value):
            raise serializers.ValidationError("Email cannot start with a number or special character.")
        return value

    def validate_password(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Password must be at least 5 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[\W_]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def validate_name(self, value):
        if re.search(r'[^a-zA-Z\s]', value):
            raise serializers.ValidationError("Name cannot include numbers or special characters (only spaces are allowed).")
        return value

    def validate_address(self, value):
        if re.match(r'^[\d\W]', value):
            raise serializers.ValidationError("Address cannot start with a number or special character.")
        return value

    def validate(self, data):
        if not data.get('email'):
            raise serializers.ValidationError({"email": "Email field is required."})
        if not data.get('name'):
            raise serializers.ValidationError({"name": "Name field is required."})
        if not data.get('phone'):
            raise serializers.ValidationError({"phone": "Phone field is required."})
        if not data.get('password'):
            raise serializers.ValidationError({"password": "Password field is required."})
        if not data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Confirm Password field is required."})
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"password": "Password and Confirm Password do not match."})
        if not data.get('role'):
            raise serializers.ValidationError({"role": "Role field is required."})
        if not data.get('address'):
            raise serializers.ValidationError({"address": "Address field is required."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            role=validated_data['role'],
            address=validated_data['address']
        )
        return user
