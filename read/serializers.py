from rest_framework import serializers
from rest_framework.authtoken.models import Token

from read.models import *
import pytz

# New Zealand Timezone
NZST = pytz.timezone("Pacific/Auckland")

'''
Serializers convert models to JSON data format
Included fields for:
    Formatted date value with time in Hours, Minutes and Seconds
    Date only
'''


class SensorDataSerializer(serializers.ModelSerializer):

    formatted_date = serializers.SerializerMethodField()
    date_only = serializers.SerializerMethodField()

    def get_formatted_date(self, obj):
        dateobj = obj.create_at.astimezone(tz=NZST)
        return dateobj.date().__str__() + " : " + dateobj.strftime('%H:%M:%S')

    def get_date_only(self, obj):
        dateobj = obj.create_at.astimezone(tz=NZST)
        return dateobj.date().__str__()

    class Meta:
        model = Sensor_Data
        fields = ('id', 'temp', 'humidity', 'soil_moisture', 'light_intensity', 'create_at', 'formatted_date', 'date_only')
