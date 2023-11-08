from apscheduler.schedulers.background import BackgroundScheduler
from urllib.request import urlopen
import json
from read.serializers import *
from read.models import Sensor_Data
from iot_api_client import Configuration, ApiClient
from iot_api_client.apis.tags.properties_v2_api import PropertiesV2Api
from openapi_client.rest import ApiException
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from djangoProject.settings import env

THING_ID = env.str("THING_ID")
CLIENT_ID = env.str("CLIENT_ID")
CLIENT_SECRET = env.str("CLIENT_SECRET")
TEMPERATURE_ID = env.str("TEMPERATURE_ID")
HUMIDITY_ID = env.str("HUMIDITY_ID")
SOIL_ID = env.str("SOIL_ID")
LIGHT_ID = env.str("LIGHT_ID")
DEVICE_ID = env.str("DEVICE_ID")


def created_new_record(humidity, temp, soil, light):
    try:
        new_row = Sensor_Data.objects.create(humidity=humidity,
                                             temp=temp,
                                             soil_moisture=soil,
                                             light_intensity=light)
        return True
    except:
        return False


# def read_raspberry_pi():
#     url = "http://192.168.181.33:5000/read"
#     response = urlopen(url)
#     data_json = json.loads(response.read())
#     while not is_valid_reading_data(data_json["humidity"],
#                                     data_json["pressure"],
#                                     data_json["temp"]):
#         response = urlopen(url)
#         data_json = json.loads(response.read())
#     print(data_json)
#     if created_new_record(1, data_json["humidity"],
#                           data_json["pressure"], data_json["temp"]):
#         print("reading success")
#     else:
#         print("reading failed")

## create function for training

def read_property(properties, PROPERTY_ID):
    try:
        path_params = {
            'id': THING_ID,
            'pid': PROPERTY_ID,
        }
        query_params = {
        }
        # show properties_v2
        print(THING_ID)
        print(PROPERTY_ID)
        # api_response = properties.properties_v2_show(THING_ID, PROPERTY_ID)
        api_response = properties.properties_v2_show(path_params=path_params, query_params=query_params)
        # This prints out the whole response
        print(api_response)
        # This shows how to extract the last_value
        print("\nVaraible {} = {}".format(api_response.response.json()['variable_name'],
                                          api_response.response.json()['last_value']))
        api_response.response.json()
        return api_response.response.json()['last_value']
    except ApiException as e:
        print("Exception when calling PropertiesV2Api->propertiesV2Show: %s\n" % e)
        return None


def read_arduino():
    oauth_client = BackendApplicationClient(client_id=CLIENT_ID)
    token_url = "https://api2.arduino.cc/iot/v1/clients/token"
    oauth = OAuth2Session(client=oauth_client)
    token = oauth.fetch_token(
        token_url=token_url,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        include_client_id=True,
        audience="https://api2.arduino.cc/iot",
    )
    print("Got a token, expires in {} seconds\n".format(token.get("expires_in")))
    client_config = Configuration(host="https://api2.arduino.cc/iot")
    # client_config.debug = True
    client_config.access_token = token.get("access_token")
    # Create the iot-api Python client with the given configuration
    client = ApiClient(client_config)

    properties = PropertiesV2Api(client)

    temp = read_property(properties, TEMPERATURE_ID)
    humidity = read_property(properties, HUMIDITY_ID)
    soil = read_property(properties, SOIL_ID)
    light = read_property(properties, LIGHT_ID)
    if created_new_record(temp=temp, humidity=humidity, soil=soil, light=light):
        print("new record created")
        ## Add testing model
    else:
        print("something wrong")


def start():
    scheduler = BackgroundScheduler()
    ### add job for training and stuff
    scheduler.add_job(read_arduino, 'interval', seconds=900)
    test()


def test():
    obj = Sensor_Data.objects.create(temp=10, humidity=10, soil_moisture=10, light_intensity=10)
    serializer = SensorDataSerializer(obj)
    print(serializer.data)
