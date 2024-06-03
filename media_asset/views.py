from django.shortcuts import render
from . serializers import CreateBillboardSerializer, AssetSerializer
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, AllowAny
from authentication.models import AnsaaUser
from todo.models import Task
from . models import Billboards
from drf_spectacular.utils import extend_schema


class CreateAssetAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateBillboardSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateBillboardSerializer(data=request.data)
        user = request.user.id
        
        if serializer.is_valid():
            serializer.save(user_id=user)

            add_media_task = Task.objects.get(user=user, title="Add a Media Asset")
            add_media_task.is_completed = True
            add_media_task.save()

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


@extend_schema(
    description="The endpoint is use to filter media assets by (asset type, zone and vacancy).",
    summary='Media Search(Filter) endpoint'
)
class AssetSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AssetSerializer

    def get(self, request, *args, **kwargs):
        # Retrieve query parameters
        asset_type = request.query_params.get('asset_type', None)
        zone = request.query_params.get('zone', None)
        vacancy = request.query_params.get('vacancy', None)
        # city = request.query_params.get('city', None)

        # Filter billboards based on query parameters
        assets = Billboards.objects.filter(user=request.user)
        if asset_type:
            assets = assets.filter(asset_type=asset_type)
        if zone:
            assets = assets.filter(zone=zone)
        # if city:
        #     assets = assets.filter(city__icontains=city)
        if vacancy is not None:
            assets = assets.filter(vacancy=vacancy)

        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)