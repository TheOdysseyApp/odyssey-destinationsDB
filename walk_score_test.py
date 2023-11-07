import boto3
import requests

dynamodb = boto3.resource('dynamodb')



class WalkscoreAPI:
    def __init__(self, wsapikey, output='json'):
        self.wsapikey = wsapikey
        self.output = output
        self.base_uri = 'http://api.walkscore.com'

    def fetch(self, request):
        response = requests.get(request)
        code = response.status_code

        if code != 200:
            return f'Server response code: {code}'
        
        return response.json()

    def get_walkscore(self, latitude, longitude, address):
        if not latitude or not longitude or not address:
            return 'Required fields are empty.'

        request = f'{self.base_uri}/score?format={self.output}&wsapikey={self.wsapikey}&lat={latitude}&lon={longitude}&bike=1&transit=1'
        return self.fetch(request)

    def get_transit_score(self, latitude, longitude, city, state):
        if not latitude or not longitude or not city or not state:
            return 'Required fields are empty.'

        request = f'{self.base_uri}/transit/score/?wsapikey={self.wsapikey}&lat={latitude}&lon={longitude}&city={city}&state={state}&format={self.output}&bike=1&transit=1'
        return self.fetch(request)
    


    def get_transit_stop_search(self):
        pass

    def get_transit_network_search(self):
        pass

    def get_transit_stop_details(self):
        pass

    def get_transit_route_details(self):
        pass

    def get_transit_supported_cities(self):
        pass

    def response_code_msg(self, code):
        messages = {
            1: 'Walk Score successfully returned.',
            2: 'Score is being calculated and is not currently available.',
            30: 'Invalid latitude/longitude.',
            31: 'Walk Score API internal error.',
            40: 'Your WSAPIKEY is invalid.',
            41: 'Your daily API quota has been exceeded.',
            42: 'Your IP address has been blocked.',
        }
        return messages.get(code, 'Sorry, response code is unknown.')
    
    
def get_walkscore_response(wsapikey, latitude, longitude, address):
    walkscore_api = WalkscoreAPI(wsapikey)
    response = walkscore_api.get_walkscore(latitude, longitude, address)
    return response

def scan_dynamodb_table(table_name):
    table = dynamodb.Table(table_name)
    response = table.scan()
    return response.get('Items', [])

def update_all_transportation_data(wsapikey, table_name):
    items = scan_dynamodb_table(table_name)
    for item in items:
        city_name = item.get('city')
        latitude = item.get('latitude')
        longitude = item.get('longitude')

        if latitude and longitude:
            walkscore_response = get_walkscore_response(wsapikey, latitude, longitude, city_name)
            
            if walkscore_response.get('status') == 1:
                walkscore = int(walkscore_response.get('walkscore', 0))  # Default to 0 if not found
                bike_score = int(walkscore_response.get('bike', {}).get('score', 0))  # Default to 0 if not found
                transit_score = int(walkscore_response.get('transit', {}).get('score', 0))  # Default to 0 if not found
                
                transportation_data = {
                    "bike_score": bike_score,
                    "walk_score": walkscore,
                    "transit_score": transit_score
                }

                upload_transportation_data(table_name, city_name, transportation_data)
            else:
                print(f"Error fetching Walkscore data for {city_name}: {walkscore_response}")
    
    
def upload_transportation_data(table_name, city_name, transportation_data):
    table = dynamodb.Table(table_name)
    update_expression = "set bike_score = :b, walk_score = :w, transit_score = :t"
    values = {
        ":b": transportation_data['bike_score'],
        ":w": transportation_data['walk_score'],
        ":t": transportation_data['transit_score']
    }
    table.update_item(
        Key={
            'city': city_name
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=values
    )


if __name__ == "__main__":
    wsapikey = ''
    # latitude = 40.7128  
    # longitude = -74.0060 
    # address = '123 Main St, City, Country'

    # walkscore_response = get_walkscore_response(wsapikey, latitude, longitude, address)
    # print(walkscore_response)

    table_name = 'travel-destination'  

    update_all_transportation_data(wsapikey, table_name)