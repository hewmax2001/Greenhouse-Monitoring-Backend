from pprint import pprint

import iot_api_client as iot
import iot_api_client.apis.tags.properties_v2_api as PropertiesV2Api
from openapi_client.rest import ApiException
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

###################################################################################
# Secret keys and stuff
###################################################################################
CLIENT_ID     = "IeUGUBJERb0coswZ1ZRxk9dVb38YB0gg"
CLIENT_SECRET = "n1At9BfKDDp81jadw26HUOtyyre5QkILrtTz0an2xAvAZv2kX7zXvUqwNQOxPRcD"
THING_ID      = "73555be9-fcad-4aac-8099-c56870b40ebb"
DEVICE_ID     = "efbbf747-1e4d-4e17-ab1a-0db2c4c0deb8"
PROPERTY_ID   = "cb20cec4-b272-4f87-8703-4bc424e23a30"  # temperature_state

###################################################################################
# Generate an access token
# Follows example from:
# https://github.com/arduino/iot-client-py/blob/master/example/main.py
###################################################################################
oauth_client = BackendApplicationClient(client_id=CLIENT_ID)
token_url = "https://api2.arduino.cc/iot/v1/clients/token"
oauth = OAuth2Session(client=oauth_client)

# This will fire an actual HTTP call to the server to exchange client_id and
# client_secret with a fresh access token
token = oauth.fetch_token(
    token_url=token_url,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    include_client_id=True,
    audience="https://api2.arduino.cc/iot",
)

# If we get here we got the token, print its expiration time
print("Got a token, expires in {} seconds\n".format(token.get("expires_in")))

######################################################################
# Show a property of my Thing.
# Follows example from Aduino IoT API documentation:
# https://www.arduino.cc/reference/en/iot/api/#api-PropertiesV2-propertiesV2Show
######################################################################

# Now we setup the iot-api Python client, first of all create a
# configuration object. The access token goes in the config object.
client_config = iot.Configuration(host="https://api2.arduino.cc/iot")
# client_config.debug = True
client_config.access_token = token.get("access_token")
# Create the iot-api Python client with the given configuration
client = iot.ApiClient(client_config)

properties = PropertiesV2Api.PropertiesV2Api(client)

try:
    # show properties_v2
    path_params = {
        'id': THING_ID,
        'pid': PROPERTY_ID,
    }
    query_params = {
    }
    api_response = properties.properties_v2_show(path_params=path_params, query_params=query_params)
    # This prints out the whole response
    pprint(api_response.response.json()['tag'])
    # This shows how to extract the last_value
    print("\nVaraible {} = {}".format(api_response.response.json()['variable_name'], api_response.response.json()['last_value']))
    api_response.response.json()
except ApiException as e:
    print("Exception when calling PropertiesV2Api->propertiesV2Show: %s\n" % e)
