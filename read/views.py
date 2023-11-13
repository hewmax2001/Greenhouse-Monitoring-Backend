import json
from datetime import datetime
from uuid import uuid4

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from read.models import Sensor_Data, AlertProfile
from read.serializers import SensorDataSerializer, AlertProfileSerializer
import datetime as DT

from read.alert_notification import start_notify

import pytz

# New Zealand Timezone
NZST = pytz.timezone("Pacific/Auckland")

# Returns all sensor data records according to a given date attached to a POST request
@api_view(['POST'])
def get_sensordata_date(request):
    # Truncates date attached to request
    date = request.POST["date"][:10]
    print(date)
    records = []
    # Compares all sensor data record's create date with request's date
    for data in Sensor_Data.objects.all():
        # Append to array if associated date
        if data.create_at.astimezone(tz=NZST).__str__() == date:
            print(data.create_at.astimezone(tz=NZST).__str__())
            records.append(data)

    # Returns serialized JSON data
    serializer = SensorDataSerializer(records, many=True)
    return Response(serializer.data)


# Returns the most recent sensor data record created
@api_view(['GET'])
def get_latest_sensordata(request):
    try:
        # Last record of all objects
        record = Sensor_Data.objects.all().last()
        # Returns serialized JSON data
        serializer = SensorDataSerializer(record)
        return Response(serializer.data)
    except Sensor_Data.DoesNotExist:
        # Return 404 if no latest record
        return Response(status=status.HTTP_404_NOT_FOUND)


# Returns the average sensor data values for the past 7 days
@api_view(['GET'])
def get_past_week(request):
    # Get today
    today = DT.date.today()
    records = []
    # From today to 7 days ago
    for i in range(7):
        # Decrement day
        day = today - DT.timedelta(days=i)
        # ISO format required
        iso = day.isoformat()
        # Return average of day
        data = get_day(iso)
        # Append to array
        records.append(data)
    # Return JSON array of average sensor data for the past 7 days
    serializer = SensorDataSerializer(records, many=True)
    return Response(serializer.data)


# Returns the average sensor data values for a given day in ISO format
def get_day(day):
    records = []
    # Define avg variables
    avg_temp = 0
    avg_hum = 0
    avg_soil = 0
    avg_light = 0
    # Iterate through all records
    for data in Sensor_Data.objects.all():
        # If corresponds with date
        if data.create_at.date().__str__() == day:
            # Append to array
            records.append(data)
            # Add to average to get total sum of values
            avg_temp += data.temp
            avg_hum += data.humidity
            avg_soil += data.soil_moisture
            avg_light += data.light_intensity

    # Divide the sum of all variables by no. of records
    length = records.__len__()
    if length <= 0:
        return None
    avg_temp /= length
    avg_hum /= length
    avg_soil /= length
    avg_light /= length
    # Create temporary record to return
    data = Sensor_Data(temp=avg_temp, humidity=avg_hum, soil_moisture=avg_soil, light_intensity=avg_light)
    # Set date of temp record corresponding to parameter
    date_format = '%Y-%m-%d'
    date_obj = datetime.strptime(day, date_format)
    data.create_at = date_obj
    # Return temp record
    return data


@api_view(['POST'])
def get_alert_profile(request):
    data = json.loads(request.body)
    print(data["expo_token"])
    user_token = data["expo_token"]

    try:
        profile = AlertProfile.objects.get(expoUserToken=user_token)
    except:
        return Response({'message' : 'No profile with user token exists'})

    serializer = AlertProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['GET'])
def create_alert_profile(request):

    user_token = uuid4()
    subscription_token = uuid4()

    profile = AlertProfile.objects.create(expoUserToken=user_token, subscriptionToken=subscription_token)

    serializer = AlertProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['POST'])
def set_temperature_alerts(request):
    user_token = request.POST["expo_token"]

    max_temp = request.POST["max_temp"]
    min_temp = request.POST["min_temp"]

    if max_temp == 'None':
        max_temp = None

    if min_temp == 'None':
        min_temp = None

    profile = AlertProfile.objects.get(expoUserToken=user_token)
    if not profile:
        return Response({'message': 'No profile with user token exists'})

    profile.maxTemp = max_temp
    profile.minTemp = min_temp
    profile.save()

    return Response({'message': 'Temperature thresholds have been updated'})


@api_view(['POST'])
def set_humidity_alerts(request):
    user_token = request.POST["expo_token"]

    max_hum = request.POST["max_hum"]
    min_hum = request.POST["min_hum"]

    if max_hum == 'None':
        max_hum = None

    if min_hum == 'None':
        min_hum = None

    profile = AlertProfile.objects.get(expoUserToken=user_token)
    if not profile:
        return Response({'message': 'No profile with user token exists'})

    profile.maxHumidity = max_hum
    profile.minHumidity = min_hum
    profile.save()

    return Response({'message': 'Humidity thresholds have been updated'})


@api_view(['POST'])
def set_soil_moisture_alerts(request):
    user_token = request.POST["expo_token"]

    max_soil = request.POST["max_soil"]
    min_soil = request.POST["min_soil"]

    if max_soil == 'None':
        max_soil = None

    if min_soil == 'None':
        min_soil = None

    profile = AlertProfile.objects.get(expoUserToken=user_token)
    if not profile:
        return Response({'message': 'No profile with user token exists'})

    profile.maxSoil = max_soil
    profile.minSoil = min_soil
    profile.save()

    return Response({'message': 'Soil Moisture thresholds have been updated'})


@api_view(['POST'])
def set_light_intensity_alerts(request):
    user_token = request.POST["expo_token"]

    max_light = request.POST["max_light"]
    min_light = request.POST["min_light"]

    if max_light == 'None':
        max_light = None

    if min_light == 'None':
        min_light = None

    profile = AlertProfile.objects.get(expoUserToken=user_token)
    if not profile:
        return Response({'message': 'Error: No profile with user token exists'})

    profile.maxLight = max_light
    profile.minLight = min_light
    profile.save()

    return Response({'message': 'Light Intensity thresholds have been updated'})


@api_view(['GET'])
def test_notify(request):
    sensor_obj = Sensor_Data.objects.create(temp=60, humidity=0, soil_moisture=0, light_intensity=0)
    start_notify(sensor_obj)

    return Response({'message': 'This works'})
