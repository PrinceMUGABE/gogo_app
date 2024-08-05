import base64
from rest_framework import serializers
from .models import Freelancer

class FreelancerSerializer(serializers.ModelSerializer):
    national_id_card = serializers.SerializerMethodField()
    driving_license = serializers.SerializerMethodField()

    class Meta:
        model = Freelancer
        fields = '__all__'

    def get_national_id_card(self, obj):
        if obj.national_id_card:
            return base64.b64encode(obj.national_id_card).decode('utf-8')
        return None

    def get_driving_license(self, obj):
        if obj.driving_license:
            return base64.b64encode(obj.driving_license).decode('utf-8')
        return None

class FreelancerCreateSerializer(serializers.ModelSerializer):
    national_id_card = serializers.ImageField(required=False)
    driving_license = serializers.ImageField(required=False)

    class Meta:
        model = Freelancer
        exclude = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        if 'national_id_card' in validated_data:
            validated_data['national_id_card'] = validated_data['national_id_card'].read()
        if 'driving_license' in validated_data:
            validated_data['driving_license'] = validated_data['driving_license'].read()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'national_id_card' in validated_data:
            validated_data['national_id_card'] = validated_data['national_id_card'].read()
        if 'driving_license' in validated_data:
            validated_data['driving_license'] = validated_data['driving_license'].read()

        return super().update(instance, validated_data)
