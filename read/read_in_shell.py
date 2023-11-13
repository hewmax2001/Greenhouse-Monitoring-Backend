from read.serializers import *
from read.models import Sensor_Data
from iot_api_client import Configuration, ApiClient
from iot_api_client.apis.tags.properties_v2_api import PropertiesV2Api
from openapi_client.rest import ApiException
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from djangoProject.settings import env
from read.alert_notification import start_notify

# Defining variables stored in .env file
THING_ID = env.str("THING_ID")
CLIENT_ID = env.str("CLIENT_ID")
CLIENT_SECRET = env.str("CLIENT_SECRET")
TEMPERATURE_ID = env.str("TEMPERATURE_ID")
HUMIDITY_ID = env.str("HUMIDITY_ID")
SOIL_ID = env.str("SOIL_ID")
LIGHT_ID = env.str("LIGHT_ID")
DEVICE_ID = env.str("DEVICE_ID")

# Setting up API values
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

#temp
try:
    path_params = {
        'id': THING_ID,
        'pid': TEMPERATURE_ID,
    }
    query_params = {
    }

    api_response = properties.properties_v2_show(path_params=path_params, query_params=query_params)
    # This prints out the whole response
    print(api_response)
    # This shows how to extract the last_value
    print("\nVaraible {} = {}".format(api_response.response.json()['variable_name'],
                                      api_response.response.json()['last_value']))
    api_response.response.json()
    temp =  api_response.response.json()['last_value']
except ApiException as e:
    print("Exception when calling PropertiesV2Api->propertiesV2Show: %s\n" % e)
    temp = None

#humidity
try:
    path_params = {
        'id': THING_ID,
        'pid': HUMIDITY_ID,
    }
    query_params = {
    }

    api_response = properties.properties_v2_show(path_params=path_params, query_params=query_params)
    # This prints out the whole response
    print(api_response)
    # This shows how to extract the last_value
    print("\nVaraible {} = {}".format(api_response.response.json()['variable_name'],
                                      api_response.response.json()['last_value']))
    api_response.response.json()
    humidity =  api_response.response.json()['last_value']
except ApiException as e:
    print("Exception when calling PropertiesV2Api->propertiesV2Show: %s\n" % e)
    humidity = None

#soil
try:
    path_params = {
        'id': THING_ID,
        'pid': SOIL_ID,
    }
    query_params = {
    }

    api_response = properties.properties_v2_show(path_params=path_params, query_params=query_params)
    # This prints out the whole response
    print(api_response)
    # This shows how to extract the last_value
    print("\nVaraible {} = {}".format(api_response.response.json()['variable_name'],
                                      api_response.response.json()['last_value']))
    api_response.response.json()
    soil =  api_response.response.json()['last_value']
except ApiException as e:
    print("Exception when calling PropertiesV2Api->propertiesV2Show: %s\n" % e)
    soil = None

#light
try:
    path_params = {
        'id': THING_ID,
        'pid': LIGHT_ID,
    }
    query_params = {
    }

    api_response = properties.properties_v2_show(path_params=path_params, query_params=query_params)
    # This prints out the whole response
    print(api_response)
    # This shows how to extract the last_value
    print("\nVaraible {} = {}".format(api_response.response.json()['variable_name'],
                                      api_response.response.json()['last_value']))
    api_response.response.json()
    light =  api_response.response.json()['last_value']
except ApiException as e:
    print("Exception when calling PropertiesV2Api->propertiesV2Show: %s\n" % e)
    light = None

obj = Sensor_Data.objects.create(temp=temp, humidity=humidity, soil_moisture=soil, light_intensity=light)
serializer = SensorDataSerializer(obj)
print(serializer.data)

# Notifying active users
start_notify(obj)