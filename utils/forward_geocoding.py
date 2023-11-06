import requests

def get_lat_lon_from_city_country(city, country):
    # Endpoint for Nominatim's geocoding service, including the country in the query
    url = f"https://nominatim.openstreetmap.org/search?city={city}&country={country}&format=json"
    response = requests.get(url)

    # Check if we got a valid response
    if response.status_code == 200:
        data = response.json()

        if not data:
            print(f"No results found for {city}, {country}")
            return None, None

        # Extract latitude and longitude from the first result
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    else:
        print(f"API request failed with status code {response.status_code}")
        return None, None

# Test the function with city and country
city = "Osaka"
country = "Japan"
lat, lon = get_lat_lon_from_city_country(city, country)
if lat and lon:
    print(f"Latitude and Longitude for {city}, {country}: {lat}, {lon}")