from rest_framework import serializers
from rest_framework.authtoken.models import Token

from read.models import *

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor_Data
        fields = "__all__"