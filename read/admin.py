from django.contrib import admin

from read.models import Sensor_Data

# Register your models here.

class Sensor_Data_Admin(admin.ModelAdmin):
    list_display = ['temp', 'humidity', 'soil_moisture', 'light_intensity', 'create_at']

admin.site.register(Sensor_Data, Sensor_Data_Admin)
