import requests

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

        request = f'{self.base_uri}/score?format={self.output}&wsapikey={self.wsapikey}&lat={latitude}&lon={longitude}&address={address}'
        return self.fetch(request)

    def get_transit_score(self, latitude, longitude, city, state, country, research):
        if not latitude or not longitude or not city or not state:
            return 'Required fields are empty.'

        request = f'{self.base_uri}/transit/score/?wsapikey={self.wsapikey}&lat={latitude}&lon={longitude}&city={city}&state={state}&format={self.output}'
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


if __name__ == "__main__":
    wsapikey = '44b56077f3bb3c2aa17c974ed75414b7'
    latitude = 40.7128  
    longitude = -74.0060 
    address = '123 Main St, City, Country'

    walkscore_response = get_walkscore_response(wsapikey, latitude, longitude, address)
    print(walkscore_response)