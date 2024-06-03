from media_asset.models import Billboards
from rest_framework import serializers


class ReportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Billboards
        fields = ['date','vacancy']