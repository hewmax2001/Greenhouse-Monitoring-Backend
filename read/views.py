from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from read.models import Sensor_Data
from read.serializers import SensorDataSerializer
import datetime as DT


# Returns all sensor data records according to a given date attached to a POST request
@api_view(['POST'])
def get_sensordata_date(request):
    # Truncates date attached to request
    date = request.POST["date"][:10]
    records = []
    # Compares all sensor data record's create date with request's date
    for data in Sensor_Data.objects.all():
        # Append to array if associated date
        if data.create_at.date().__str__() == date:
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
