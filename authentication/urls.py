from django.urls import path
from . import views

urlpatterns = [
    path('auth/otp-request/', views.RequestOTP.as_view()),
    path('auth/logout/', views.LogoutView.as_view()),
    path('auth/validate-otp/', views.ValidateOTPView.as_view()),
    path('auth/profile/', views.UserProfileViews.as_view()),
    path('auth/register/', views.RegistrationAPIView.as_view()),
    path('auth/login/', views.LoginAPIView.as_view()),
]
