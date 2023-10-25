import datetime

from django.db import models


# Create your models here.
class Sensor(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    # url
    # reading_time
    # warning

    def __str__(self):
        return self.name


class Sensor_Data(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True)
    temp = models.IntegerField(null=True)
    humidity = models.IntegerField(null=True)
    soil_moisture = models.IntegerField(null=True)
    light_intensity = models.IntegerField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sensor.name + " - " + self.create_at.__str__()