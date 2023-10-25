from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from read.models import Sensor_Data
from read.serializers import SensorDataSerializer
import datetime as DT


# Create your views here.
@api_view(['POST'])
def get_sensordata_date(request):
    date = request.POST["date"][:10]
    records = []
    for data in Sensor_Data.objects.all():
        if data.create_at.date().__str__() == date:
            records.append(data)

    serializer = SensorDataSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def get_sensordata_date_avg(request):
    date = request.POST["date"][:10]

    data = get_day(date)
    if data == None:
        return Response("No records from this date")
    serializer = SensorDataSerializer(data, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_latest_sensordata(request):
    try:
        record = Sensor_Data.objects.all().last()
        serializer = SensorDataSerializer(record)
        return Response(serializer.data)
    except Sensor_Data.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_past_week(request):
    today = DT.date.today()
    records = []
    for i in range(7):
        day = today - DT.timedelta(days=i)
        iso = day.isoformat()
        print(f"{i} days ago: {iso}")
        data = get_day(iso)
        records.append(data)
    serializer = SensorDataSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_past_week_temp(request):
    today = DT.date.today()
    records = []
    for i in range(7):
        day = today - DT.timedelta(days=i)
        iso = day.isoformat()
        data = get_day(iso)
        records.append(data)
    serializer = SensorDataSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_past_week_hum(request):
    today = DT.date.today()
    records = []
    for i in range(7):
        day = today - DT.timedelta(days=i)
        iso = day.isoformat()
        data = get_day(iso)
        records.append(data.humidity)
    return Response(records)


@api_view(['GET'])
def get_past_week_soil(request):
    today = DT.date.today()
    records = []
    for i in range(7):
        day = today - DT.timedelta(days=i)
        iso = day.isoformat()
        data = get_day(iso)
        records.append(data.soil_moisture)

    return Response(records)


@api_view(['GET'])
def get_past_week_light(request):
    today = DT.date.today()
    records = []
    for i in range(7):
        day = today - DT.timedelta(days=i)
        iso = day.isoformat()
        data = get_day(iso)
        records.append(data.light_intensity)
    return Response(records)


def get_day(day):
    records = []
    avg_temp = 0
    avg_hum = 0
    avg_soil = 0
    avg_light = 0
    for data in Sensor_Data.objects.all():
        if data.create_at.date().__str__() == day:
            records.append(data)
            avg_temp += data.temp
            avg_hum += data.humidity
            avg_soil += data.soil_moisture
            avg_light += data.light_intensity

    length = records.__len__()
    if length <= 0:
        return None
    avg_temp /= length
    avg_hum /= length
    avg_soil /= length
    avg_light /= length
    data = Sensor_Data(temp=avg_temp, humidity=avg_hum, soil_moisture=avg_soil, light_intensity=avg_light)
    data.create_at = day
    return data
