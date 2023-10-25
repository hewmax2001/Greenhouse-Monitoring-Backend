from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from read.serializers import *


class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = Sensor_Data.objects.all()
    serializer_class = SensorDataSerializer
