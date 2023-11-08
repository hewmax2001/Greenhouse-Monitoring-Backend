from rest_framework import serializers
from rest_framework.authtoken.models import Token

from read.models import *
import pytz

NZST = pytz.timezone("Pacific/Auckland")


class SensorDataSerializer(serializers.ModelSerializer):

    formatted_date = serializers.SerializerMethodField()

    def get_formatted_date(self, obj):
        dateobj = obj.create_at.astimezone(tz=NZST)
        print("works")
        return dateobj.date().__str__() + " : " + dateobj.time().__str__()

    class Meta:
        model = Sensor_Data
        fields = ('temp', 'humidity', 'soil_moisture', 'light_intensity', 'create_at', 'formatted_date')
