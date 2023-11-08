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
        return self.temp.__str__() + " " + self.humidity.__str__() + " " + self.soil_moisture.__str__() + " " + self.light_intensity.__str__() + " " + self.create_at.__str__()

