import datetime

from django.db import models


# Create your models here.

class Sensor_Data(models.Model):
    temp = models.IntegerField(null=True)
    humidity = models.IntegerField(null=True)
    soil_moisture = models.IntegerField(null=True)
    light_intensity = models.IntegerField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.create_at

