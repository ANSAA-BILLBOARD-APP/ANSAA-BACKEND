from django.shortcuts import render
from . serializers import TaskSerializer, CreateBillboardSerializer, AssetSerializer
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, AllowAny
from authentication.models import AnsaaUser, Task
from . models import Billboards

class TaskAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)


class CreateAssetAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateBillboardSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateBillboardSerializer(data=request.data)
        user = request.user.id  # Assuming authenticated user is provided in the request
        
        if serializer.is_valid():
            serializer.save(user_id=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssetRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Billboards.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)




class AssetListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AssetSerializer

    def get_queryset(self):
        user = self.request.user
        return Billboards.objects.filter(user=user)