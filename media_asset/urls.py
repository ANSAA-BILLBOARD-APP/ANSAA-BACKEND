from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.TaskAPIView.as_view()),
    path('create/', views.CreateBillboardAPIView.as_view()),
]
