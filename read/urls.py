from django.urls import path, include
from rest_framework.routers import DefaultRouter

from read.views import *
from read.viewsets import SensorDataViewSet

router = DefaultRouter()
router.register("sensordata", SensorDataViewSet)

'''
Associating the URLs of the application with the views
Basis of the API
'''

urlpatterns = [
    path("", include(router.urls)),

    path("sensordata_date/", get_sensordata_date),
    path("sensordata_latest/", get_latest_sensordata),
    path("sensordata_week/", get_past_week),

    path("get_alert_profile/", get_alert_profile),
    path("create_alert_profile/", create_alert_profile),

    path("set_temp_alert/", set_temperature_alerts),
    path("set_hum_alert/", set_humidity_alerts),
    path("set_soil_alert/", set_soil_moisture_alerts),
    path("set_light_alert/", set_light_intensity_alerts),

    path("test/", test_notify),
]
