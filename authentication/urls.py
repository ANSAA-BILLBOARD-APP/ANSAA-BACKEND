from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/otp-request/', views.RequestOTP.as_view()),
    path('api/logout/', views.LogoutView.as_view()),
    path('api/validate-otp/', views.ValidateOTPView.as_view()),
    path('api/profile/', views.UserProfileViews.as_view()),
    path('api/login/', views.LoginAPIView.as_view()),
    path("api/api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema")),
]
