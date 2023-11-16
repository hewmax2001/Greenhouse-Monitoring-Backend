import requests
from read.models import Sensor_Data, AlertProfile
from datetime import datetime

def start_notify(sensor_obj):
    temp = sensor_obj.temp
    hum = sensor_obj.humidity
    soil = sensor_obj.soil_moisture
    light = sensor_obj.light_intensity

    temp_alerts(temp)
    hum_alerts(hum)
    soil_alerts(soil)
    light_alerts(light)


def temp_alerts(temp):
    temp_max_qset = AlertProfile.objects.filter(maxTemp__lt=temp)
    temp_min_qset = AlertProfile.objects.filter(minTemp__gt=temp)

    for profile in temp_max_qset:
        title = "Temperature Alert!"
        body = "Maximum Temperature Threshold Breached!"
        send_notification(profile, title, body)

    for profile in temp_min_qset:
        title = "Temperature Alert!"
        body = "Minimum Temperature Threshold Breached!"
        send_notification(profile, title, body)


def hum_alerts(hum):
    hum_max_qset = AlertProfile.objects.filter(maxHumidity__lt=hum)
    hum_min_qset = AlertProfile.objects.filter(minHumidity__gt=hum)

    for profile in hum_max_qset:
        title = "Humidity Alert!"
        body = "Maximum Humidity Threshold Breached!"
        send_notification(profile, title, body)

    for profile in hum_min_qset:
        title = "Humidity Alert!"
        body = "Minimum Humidity Threshold Breached!"
        send_notification(profile, title, body)


def soil_alerts(soil):
    soil_max_qset = AlertProfile.objects.filter(maxSoil__lt=soil)
    soil_min_qset = AlertProfile.objects.filter(minSoil__gt=soil)

    for profile in soil_max_qset:
        title = "Soil Moisture Alert!"
        body = "Maximum Soil Moisture Threshold Breached!"
        send_notification(profile, title, body)

    for profile in soil_min_qset:
        title = "Soil Moisture Alert!"
        body = "Minimum Soil Moisture Threshold Breached!"
        send_notification(profile, title, body)


def light_alerts(light):
    light_max_qset = AlertProfile.objects.filter(maxLight__lt=light)
    light_min_qset = AlertProfile.objects.filter(minLight__gt=light)

    for profile in light_max_qset:
        title = "Light Intensity Alert!"
        body = "Maximum Light Intensity Threshold Breached!"
        send_notification(profile, title, body)

    for profile in light_min_qset:
        title = "Light Intensity Alert!"
        body = "Minimum Light Intensity Threshold Breached!"
        send_notification(profile, title, body)


def send_notification(profile, title, body):
    if profile.active:
        sub_id = profile.subscriptionToken
        url = 'https://app.nativenotify.com/api/indie/notification'
        json_obj = {
            'subID': sub_id,
            'appId': '14719',
            'appToken': "fS59VdsG6wSUsAUbYddt18",
            'title': title,
            'message': body,
         }

        x = requests.post(url, json=json_obj)