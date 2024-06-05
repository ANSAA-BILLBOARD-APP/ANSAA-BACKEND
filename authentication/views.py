from django.shortcuts import render
from rest_framework.exceptions import NotFound
from django.db import DatabaseError
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework import status
from . serializers import RequestOTPSerializer, LogoutSerializer, OTPVerificationSerializer, ProfileSerializer, LoginSerializer
from . models import AnsaaUser, OTP
from todo.models import Task
from . task import generate_otp, EmailThread, send_otp_email, send_otp_sms
import asyncio
from drf_spectacular.utils import extend_schema
import resend


@extend_schema(
    description="This endpoint takes either the user's email or phone in order to dispatch an OTP. Note that the user must be an Ansa authorise user.",
    summary='User OTP Request'
)
class RequestOTP(APIView):
    serializer_class = RequestOTPSerializer

    def post(self, request, format="json"):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email')
        phone_number = request.data.get('phone_number')

        # Validate email and phone number
        if (email == "") or (phone_number == ""):
            return Response({"error": "Please provide both email and phone number."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        approved_user = AnsaaUser.objects.filter(Q(email=email) | Q(phone_number=phone_number)).first()
        if not approved_user:
            return Response({'error': 'Invalid user credential'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a random 4-digit OTP
        otp_code = generate_otp()
        expiration_time = timezone.now() + timezone.timedelta(minutes=5)

        # Check if OTP already sent
        existing_otp = OTP.objects.filter(Q(email=email) | Q(phone_number=phone_number)).first()
        if existing_otp and not existing_otp.expired:
            return Response({'error': 'OTP already sent. Please check for the existing OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        # Send OTP via email
        if email:
            send_otp_email(email, otp_code)
            phone_number = approved_user.phone_number
            otp_obj, created = OTP.objects.get_or_create(email=email, phone_number=phone_number, defaults={'otp': otp_code, 'expiration_time': expiration_time})
            if not created:
                otp_obj, created = OTP.objects.get_or_create(email=email)
                otp_obj.expiration_time = expiration_time 
                otp_obj.otp = otp_code
                otp_obj.phone_number = phone_number
                otp_obj.save()
                
        # Send OTP via SMS (to be implemented)
        elif phone_number:
            send_otp_sms(phone_number, otp_code)
            email = approved_user.email
            otp_obj, created = OTP.objects.get_or_create(phone_number=phone_number, email=email, defaults={'otp': otp_code, 'expiration_time': expiration_time})
            if not created:
                otp_obj, created = OTP.objects.get_or_create(phone_number=phone_number)
                otp_obj.expiration_time = expiration_time 
                otp_obj.otp = otp_code
                otp_obj.email = email
                otp_obj.save()

        return Response({"message": "OTP generated and sent successfully."}, status=status.HTTP_201_CREATED)


@extend_schema(
    description="This endpoint takes either the user's email or phone number and a four-digit OTP and validates the user's OTP.",
    summary='User OTP verification'
)
class ValidateOTPView(APIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        email = data.get('email')
        phone_number = data.get('phone_number')
        otp = data.get('otp')

        if not (email or phone_number):
            response = {
                'error': 'Please provide either email or phone number.',
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        try:
            if email:
                otp_record = OTP.objects.get(email=email, otp=otp, verified=False)
            else:
                otp_record = OTP.objects.get(phone_number=phone_number, otp=otp, verified=False)
        except OTP.DoesNotExist:
            response = {
                'error': 'Invalid OTP.',
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        if otp_record.is_expired():
            response = {
                'error': 'OTP has expired. Please generate a new one.',
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        # Verify the OTP
        otp_record.verified = True
        otp_record.save()

        response = {
            'message': 'OTP verified.',
        }
        return Response(data=response, status=status.HTTP_200_OK)
        
@extend_schema(
    description="This endpoint takes user refresh token.",
    summary='Logout'
)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViews(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        user = request.user
        try:  
            user_profile = AnsaaUser.objects.get(pk=user.pk)
            serializer = ProfileSerializer(user_profile)
            return Response(serializer.data)
        except AnsaaUser.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, format=None):
        user = request.user
        user_profile = AnsaaUser.objects.get(pk=user.pk)
        if not user_profile:
            return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        picture = request.data.get('picture')
        if not picture:
            return Response({'error': 'Picture field is required'}, status=status.HTTP_400_BAD_REQUEST)

        user_profile.picture = picture
        user_profile.save()

        try:
            update_profile_task = Task.objects.get(user=user, title="Add a Profile Picture")
            update_profile_task.is_completed = True
            update_profile_task.save()
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data)

@extend_schema(
    description='The users "phone number" or "email" is required for authentication on this login endpoint.',
    summary='User Login'
)
class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            phone_number = serializer.validated_data.get("phone_number")
            

            #if otp is in record and it's verified
            existing_otp = OTP.objects.filter(
            Q(email=email) | Q(phone_number=phone_number)
            ).first()
            if existing_otp:
                email = existing_otp.email
                if email:
                    otp_record = OTP.objects.get(email=email, verified=True)
                    if not otp_record.is_expired():
                        user = AnsaaUser.objects.filter(email=email).first()
                        authenticated_user = authenticate(request, email=email)
                        if authenticated_user:
                            refresh = RefreshToken.for_user(authenticated_user)
                            otp_record.delete()

                            return Response({'refresh': str(refresh), 'access': str(refresh.access_token),}, status=status.HTTP_200_OK)  
                        else:
                            return Response({'error': 'Invalid user credentials'}, status.status.HTTP_400_BAD_REQUEST)
                    else:
                        otp_record.delete()
                        return Response({'error':'OTP expired, request for another'}, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({'error': 'Invalid user credentials'}, status=status.HTTP_400_BAD_REQUEST)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

