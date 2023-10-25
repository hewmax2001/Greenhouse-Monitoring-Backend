import random
from datetime import datetime, time, timedelta

from read.models import Sensor_Data


def main():
    today = datetime.today()
    soil = 34
    temp = 51
    hum = 90
    light = 1221
    for i in range(9):
        day = today - timedelta(days= 5 - i)
        start_day(day, temp, hum, soil, light)
        soil += random.choice([2, 3, 4])
        temp = random.randrange(40, 60)
        hum = random.randrange(50, 95)
        light = random.randrange(1000, 1600)


def start_day(date, temp, hum, soil, light):
    start_of_day = datetime.combine(date, time.min)
    data = Sensor_Data.objects.create(temp=temp, humidity=hum, soil_moisture=soil, light_intensity=light, create_at=date, sensor_id=1)
    data.create_at = date
    data.save()
    print(data)


