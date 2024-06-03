from django.urls import path
from . import views

urlpatterns = [
    path('api/devices/', views.DeviceListAPIView.as_view(), name='device_list'),
    path('api/devices/', views.DeviceCreateAPIView.as_view(), name='create_device'),
    path('api/devices/<int:pk>/', views.DeviceUpdateAPIView.as_view(), name='update device'),
    path('api/task/', views.TaskAPIView.as_view(), name="assigned_asset"),
]