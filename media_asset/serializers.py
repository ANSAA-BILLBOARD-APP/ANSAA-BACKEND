from authentication.models import Task
from .models import UserZone, Billboards
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title','description','is_completed','user']


class UserZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserZone
        fields = '__all__'


class CreateBillboardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Billboards
        fields = ['asset_type','category','zone','sub_zone','description'
        ,'vacancy','dimension','price','main_image','image_1','image_2','image_3'
        ,'address','city','state','country','company','phone_number','longitude','latitude','user_id']