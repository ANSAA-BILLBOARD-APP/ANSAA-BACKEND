from django.shortcuts import render
from rest_framework.exceptions import NotFound
from django.db import DatabaseError
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives, EmailMessage
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.core.mail import send_mail
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from . serializers import RequestOTPSerializer, LogoutSerializer, OTPVerificationSerializer, ProfileSerializer, RegistrationSerializer, LoginSerializer
from . models import AnsaaUser, OTP, AnsaaApprovedUser
from . task import generate_otp, EmailThread




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

        # Validate email format
        if not email.strip() or not email.isascii() or not email.lower() == email:
            return Response({"message": "Please provide a valid email address.", "status": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            email.encode('ascii')  # Additional check for valid encoding
        except UnicodeEncodeError:
            return Response({"message": "Email address contains invalid characters.", "status": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        approved_user = AnsaaApprovedUser.objects.filter(email=email).first()
        approved_user_number = AnsaaApprovedUser.objects.filter(phone_number=phone_number).first()
        if not approved_user or approved_user_number:
            return Response({'message': 'Invalid user credential'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a random 6-digit OTP
        otp_code = generate_otp()
        expiration_time = timezone.now() + timezone.timedelta(minutes=5)

        existing_otp = OTP.objects.filter(
            Q(email=email) | Q(phone_number=phone_number)
        )

        if existing_otp.exists():
            existing_otp = existing_otp.first()
            if not existing_otp.expired:
                return Response({'error': 'OTP already sent. Please check for the existing OTP.'}, status=HTTP_400_BAD_REQUEST)

        if email:
            print(f"OTP: {otp_code}")
            # Send the email with OTP
            email_subject = 'Ansaa OTP'
            template = loader.get_template('mail_template.txt')
            parameters = {'otp': otp_code}
            email_content = template.render(parameters)

            email_message = EmailMultiAlternatives(
                email_subject,
                email_content,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_message.content_subtype = 'html'

            # Start email sending thread
            EmailThread(email_message).start()

            # Store OTP and its expiration time
            otp_obj, created = OTP.objects.get_or_create(email=email, defaults={'otp': otp_code, 'expiration_time': expiration_time})
            if not created:
                otp_obj, created = OTP.objects.get_or_create(email=email)
                otp_obj.expiration_time = expiration_time 
                otp_obj.otp = otp_code
                otp_obj.save()
            
            return Response({"message": "OTP generated and sent successfully.", "status": "SUCCESS"}, status=status.HTTP_201_CREATED)
        
        elif phone_number:
            # Implement sending of OTP to phone number


            # Store OTP and its expiration time
            otp_obj, created = OTP.objects.get_or_create(email=email, defaults={'otp': otp_code, 'expiration_time': expiration_time})
            if not created:
                otp_obj, created = OTP.objects.get_or_create(email=email)
                otp_obj.expiration_time = expiration_time 
                otp_obj.otp = otp_code
                otp_obj.save()
            
            return Response({"message": "OTP generated and sent successfully."}, status=status.HTTP_201_CREATED)
        return Response({"message": "Error generating OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ValidateOTPView(APIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request):
        email = request.data.get('email')
        user_otp = request.data.get('otp')

        
        if email and user_otp:
            # Check if the OTP exists and is not expired
            otp = OTP.objects.filter(email=email).last()
            if not otp:
                response = {
                    'message': 'Invalid OTP.',
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            
            if otp.verified:
                response = {
                    "message":"email already verify please proceed to login"
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            if otp.is_expired():
                response = {
                    'message': 'OTP has expired. Please generate a new one.',
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            # Verify the OTP
            if otp.otp == user_otp:
                response = {
                    'message': 'OTP verified.',
                }
                otp.verified = True
                otp.save()
                
                return Response(data=response, status=status.HTTP_200_OK)

            response = {
                'message': 'Invalid OTP.',
                'STATUS': 'ERROR'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "message":"Fields cannot be empty"
        }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        

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
                return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)



class UserProfileViews(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        user_profile = AnsaaUser.objects.filter(email=request.user).first()
        if not user_profile:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request, format=None):
        user_profile = AnsaaUser.objects.filter(email=request.user).first()
        if not user_profile:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        picture = request.data.get('picture')
        if not picture:
            return Response({'message': 'Picture field is required'}, status=status.HTTP_400_BAD_REQUEST)

        user_profile.picture = picture
        user_profile.save()

        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data)


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get("email")
            phone_number = request.data.get('phone_number')

            print(f"phone number: {phone_number}")
            print(f"user email: {email}")

            if AnsaaUser.objects.filter(email=email).exists() or  AnsaaUser.objects.filter(phone_number=phone_number).exists():
                return Response({'message': 'User already exist'}, status=status.HTTP_400_BAD_REQUEST)

            approved_user = AnsaaApprovedUser.objects.filter(email=email).first()
            approved_user_number = AnsaaApprovedUser.objects.filter(phone_number=phone_number).first()

            if not approved_user or approved_user_number:
                return Response({'message': 'Invalid user credential'}, status=status.HTTP_400_BAD_REQUEST)

            fullname = approved_user.fullname
            phone_number = approved_user.phone_number

            otp_exist = OTP.objects.filter(email=email).first()
            otp_exist_phone = OTP.objects.filter(phone_number=phone_number).first()
            if otp_exist:

                if otp_exist.verified:
                    user_data = {
                        'email': email,
                        'phone_number': phone_number,
                        'fullname': fullname,
                    }
                    user_serializer = RegistrationSerializer(data=user_data)
                    if user_serializer.is_valid():
                        user_serializer.save()
                        user = user_serializer.instance
                        otp_exist.delete()

                        # Generate JWT token
                        refresh = RefreshToken.for_user(user)
                        access_token = str(refresh.access_token)
                        return Response({'message': 'User registered successfully', 'access_token': access_token}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'Unvarified identity'}, status=status.HTTP_400_BAD_REQUEST)

            elif otp_exist_phone:
                if otp_exist_phone.verified:
                    user_data = {
                        'email': email,
                        'phone_number': phone_number,
                        'fullname': fullname,
                    }
                    user_serializer = RegistrationSerializer(data=user_data)
                    if user_serializer.is_valid():
                        user_serializer.save()
                        user = user_serializer.instance
                        otp_exist_phone.delete()

                        # Generate JWT token
                        refresh = RefreshToken.for_user(user)
                        access_token = str(refresh.access_token)
                        return Response({'message': 'User registered successfully', 'access_token': access_token}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'Invalid user credential'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_verified():
            email = serializer.validated_data.get("email")
            phone_number = serializer.validated_data.get("otp")

            #check if otp is in record and it's verified
            existing_otp = OTP.objects.filter(
            Q(email=email) | Q(phone_number=phone_number)
            )
            if existing_otp:
                if email:
                    if existing_otp.expired:
                        user = AnsaaUser.objects.filter(email=email).first()
                        if user:
                            refresh = RefreshToken.for_user(user)
                            exist_otp.delete()

                            return Response({'refresh': str(refresh), 'access': str(refresh.access_token),}, status=status.HTTP_200_OK)  
                        else:
                            return Response({'error': 'Invalid user credentials'}, status.status.HTTP_400_BAD_REQUEST)
                    else:
                        otp_record.delete()
                        return Response({'error':'OTP expired, request for another'}, status=status.HTTP_400_BAD_REQUEST)
                elif phone_number:
                    if existing_otp.expired:
                        user = AnsaaUser.objects.filter(phone_number=phone_number).first()
                        if user:
                            refresh = RefreshToken.for_user(user)
                            exist_otp.delete()

                            return Response({'refresh': str(refresh), 'access': str(refresh.access_token),}, status=status.HTTP_200_OK)  
                        else:
                            return Response({'error': 'Invalid user credentials'}, status.status.HTTP_400_BAD_REQUEST)
                    else:
                        otp_record.delete()
                        return Response({'error':'OTP expired, request for another'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Invalid user credentials'}, status=status.HTTP_400_BAD_REQUEST)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)