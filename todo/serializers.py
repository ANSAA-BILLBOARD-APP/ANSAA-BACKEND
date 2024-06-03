from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from .models import DeviceDetail, Task



class DeviceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceDetail
        fields = ['device_name', 'device_id', 'os', 'created_at']
        read_only_fields = ['created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title','description','is_completed','user']