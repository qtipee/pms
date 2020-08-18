from rest_framework import serializers
from datetime import datetime
from .models import *

class ImageSerializer(serializers.ModelSerializer):
    # DateTime field format
    datetime = serializers.DateTimeField(format='%d.%m.%Y %H:%M')
    
    class Meta:
        model = Image
        fields = ('id', 'datetime', 'count')
