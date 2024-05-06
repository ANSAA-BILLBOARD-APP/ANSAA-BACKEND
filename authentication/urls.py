from django.urls import path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/auth/otp-request/', views.RequestOTP.as_view()),
    path('api/auth/logout/', views.LogoutView.as_view()),
    path('api/auth/validate-otp/', views.ValidateOTPView.as_view()),
    path('api/auth/profile/', views.UserProfileViews.as_view()),
    path('api/auth/register/', views.RegistrationAPIView.as_view()),
    path('api/auth/login/', views.LoginAPIView.as_view()),
    path("api/api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema")),
]
