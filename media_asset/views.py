from django.shortcuts import render
from . serializers import TaskSerializer, CreateBillboardSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from authentication.models import AnsaaUser, Task
from . models import Billboards

class TaskAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)


class CreateBillboardAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CreateBillboardSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateBillboardSerializer(data=request.data)
        user = request.user
        print(user)
        if serializer.is_valid():
            if self.all_fields_filled(serializer.validated_data):
                serializer.validated_data['status'] = 'complete'
            else:
                serializer.validated_data['status'] = 'pending'
            serializer.save(user=user)  # Assign the authenticated user as the agent
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def all_fields_filled(self, data):
        return all(value for value in data.values() if value is not None and value != '')
