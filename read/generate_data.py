import random
from datetime import datetime, time, timedelta

import pytz

NZST = pytz.timezone("Pacific/Auckland")

endate = datetime.today().astimezone(NZST)
startdate = endate - timedelta(days=14)

startday = 8
endday = 18

startnight = 21
endnight = 5

from read.models import Sensor_Data

tempday = random.randint(13, 19)
lightday = random.randint(400, 515)
tempnight = 10
lightnight = 0
nexttempday = random.randint(13, 19)
nextlightday = random.randint(400, 515)



def main():
    print(endate)
    print(startdate.hour)

    current = startdate
    soil_moisture = 81
    end_soil = soil_moisture - random.randint(3, 6)
    soil_counter = 0

    while current < endate:
        #set new temps and light
        nexttempday = random.randint(13, 19)
        nextlightday = random.randint(400, 515)
        tempnight = ((tempday + nexttempday) / 2) - random.randint(4, 6)
        lightnight = random.randint(9, 61)
        hum = random.randint(49, 68)
        if soil_counter >= 5:
            print("WATERING")
            soil_moisture = random.randint(70, 91)
        end_soil = soil_moisture - random.randint(3, 6)
        soil_counter += 1;
        current = beginday(current, soil=soil_moisture, end_soil=end_soil, hum=hum)
        soil_moisture = end_soil
    print(current)


def beginday(current, soil, end_soil, hum):
    temp = tempday
    light = lightday
    soilmod = (soil - end_soil) / (4 * 24)
    print("START DAY")

    while (current.hour != endday):
        current = current + timedelta(minutes=15)
        soil -= soilmod
        temp = tempday + random.randint(-3, 3)
        light = lightday + random.randint(-100, 100)
        newhum = hum + random.randint(-3, 5)
        sensobj = Sensor_Data.objects.create(temp=temp, humidity=newhum, light_intensity=light, soil_moisture=soil)
        sensobj.create_at = current
        sensobj.save()
        print(sensobj)

    tempmod = (tempday - tempnight) / (4 * 3)
    lightmod = (lightday - lightnight) / (4 * 3)
    print("END DAY")

    while (current.hour != startnight):
        current = current + timedelta(minutes=15)
        soil -= soilmod
        temp -= tempmod
        light -= lightmod
        newhum = hum + random.randint(-5, 3)
        sensobj = Sensor_Data.objects.create(temp=temp, humidity=newhum, light_intensity=light, soil_moisture=soil)
        sensobj.create_at = current
        sensobj.save()
        print(sensobj)

    print("START NIGHT")

    while (current.hour != endnight):
        current = current + timedelta(minutes=15)
        soil -= soilmod
        temp = tempnight + random.randint(-3, 3)
        light = lightnight + random.randint(0, 62)
        newhum = hum + random.randint(-3, 2)
        sensobj = Sensor_Data.objects.create(temp=temp, humidity=newhum, light_intensity=light, soil_moisture=soil)
        sensobj.create_at = current
        sensobj.save()
        print(sensobj)

    tempmod = (nexttempday - tempnight) / (4 * 3)
    lightmod = (nextlightday - lightnight) / (4 * 3)
    print("END NIGHT")

    while (current.hour != startday):
        current = current + timedelta(minutes=15)
        soil -= soilmod
        temp += tempmod
        light += lightmod
        newhum = hum + random.randint(-4, 4)
        sensobj = Sensor_Data.objects.create(temp=temp, humidity=newhum, light_intensity=light, soil_moisture=soil)
        sensobj.create_at = current
        sensobj.save()
        print(sensobj)

    return current;
