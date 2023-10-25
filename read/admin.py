from django.contrib import admin

from read.models import Sensor, Sensor_Data

# Register your models here.
admin.site.register(Sensor)


class Sensor_Data_Admin(admin.ModelAdmin):
    list_display = ['sensor', 'temp', 'humidity', 'create_at']

admin.site.register(Sensor_Data, Sensor_Data_Admin)
