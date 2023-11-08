from django.urls import path, include
from rest_framework.routers import DefaultRouter

from read.views import *
from read.viewsets import SensorDataViewSet

router = DefaultRouter()
router.register("sensordata", SensorDataViewSet)

urlpatterns = [
    path("", include(router.urls)),

    path("sensordata_date/", get_sensordata_date),
    path("sensordata_date_avg/", get_sensordata_date_avg),
    path("sensordata_latest/", get_latest_sensordata),
    path("sensordata_week/", get_past_week),
]
