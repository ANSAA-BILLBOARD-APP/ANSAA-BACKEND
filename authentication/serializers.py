from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from .models import AnsaaUser, OTP


class RequestOTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    phone_number = PhoneNumberField(required=False)
    
    class Meta:
        model = OTP
        fields = ["email", "phone_number"]

class OTPVerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    phone_number = PhoneNumberField(required=False)
    otp = serializers.CharField(required=True)
    
    class Meta:
        model = OTP
        fields = ["email", "phone_number", "otp"]   


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = PhoneNumberField(required=False)

    class Meta:
        model = AnsaaUser
        fields= ['email','phone_number']

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='email.email', read_only=True)
    phone_number = serializers.CharField()
    
    class Meta:
        model = AnsaaUser
        fields = ['user_id', 'email', 'phone_number', 'fullname', 'picture', 'gender']


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
