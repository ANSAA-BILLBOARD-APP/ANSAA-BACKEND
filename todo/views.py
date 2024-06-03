from django.shortcuts import render
from rest_framework.exceptions import NotFound
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework import status
from . serializers import DeviceDetailSerializer, TaskSerializer
from . models import DeviceDetail
import asyncio
from drf_spectacular.utils import extend_schema



class DeviceCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceDetailSerializer

    def post(self, request, format=None):
        serializer = DeviceDetailSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            serializer.save(user=request.user)

            try:
                update_davice_task = Task.objects.get(user=user, title="Approve Device")
                update_davice_task.is_completed = True
                update_davice_task.save()
            except Task.DoesNotExist:
                return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceDetailSerializer

    def get(self, request, format=None):
        # Retrieve all devices for the authenticated user
        devices = DeviceDetail.objects.filter(user=request.user)
        serializer = DeviceDetailSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeviceUpdateAPIView(RetrieveUpdateAPIView):
    queryset = DeviceDetail.objects.all()
    serializer_class = DeviceDetailSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class TaskAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)