import requests

def get_lat_lon_from_city(city):
    # Endpoint for Nominatim's geocoding service
    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
    response = requests.get(url)

    # Check if we got a valid response
    if response.status_code == 200:
        data = response.json()

        if not data:
            print(f"No results found for {city}")
            return None, None

        # Extract latitude and longitude from the first result
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    else:
        print(f"API request failed with status code {response.status_code}")
        return None, None

# Test the function
city = "Bangkok"
lat, lon = get_lat_lon_from_city(city)
if lat and lon:
    print(f"Latitude and Longitude for {city}: {lat}, {lon}")