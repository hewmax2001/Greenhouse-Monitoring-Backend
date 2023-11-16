from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

'''
Model representing a record of sensor data with:
    Temperature
    Humidity
    Soil Moisture
    Light Intensity
    Date of Creation
'''


class Sensor_Data(models.Model):
    temp = models.IntegerField(null=True)
    humidity = models.IntegerField(null=True)
    soil_moisture = models.IntegerField(null=True)
    light_intensity = models.IntegerField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.create_at


class AlertProfile(models.Model):
    expoUserToken = models.CharField(max_length=100, blank=False, null=False)
    subscriptionToken = models.CharField(max_length=100, blank=False, null=False)
    active = models.BooleanField(default=True)

    maxTemp = models.IntegerField(validators=[MinValueValidator(-20), MaxValueValidator(50)], null=True, default=None)
    minTemp = models.IntegerField(validators=[MinValueValidator(-20), MaxValueValidator(50)], null=True, default=None)

    maxHumidity = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, default=None)
    minHumidity = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, default=None)

    maxSoil = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, default=None)
    minSoil = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, default=None)

    maxLight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, default=None)
    minLight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2500)], null=True, default=None)
