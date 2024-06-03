from .models import UserZone, Billboards
from rest_framework import serializers


class UserZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserZone
        fields = '__all__'


class CreateBillboardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Billboards
        fields = ['asset_type','category','zone','status','sub_zone','description'
        ,'vacancy','status','dimension','price','main_image','image_1','image_2','image_3'
        ,'address','city','state','country','company','phone_number','longitude','latitude','user_id']


class AssetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Billboards
        fields = '__all__'