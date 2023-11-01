from amadeus import Client, ResponseError
from dotenv import load_dotenv
import os

load_dotenv()

def create_amadeus_client():
    amadeus = Client(
        client_id=os.getenv("AMADEUS_TEST_KEY"),
        client_secret=os.getenv("AMADEUS_TEST_SECRET")#,
        # host="production"
    )
    return amadeus
# try:
#     response = amadeus.safety.safety_rated_locations.get(longitude=117.8265, latitude=33.6846)
#     # response = amadeus.safety.safety_rated_locations.get(longitude=2.160873, latitude=41.397158)
#     print("test")
#     print(response.data)
#     print(response.data[0]["name"])
#     print(response.data[0]["safetyScores"])
#     print(response.data[0]["safetyScores"]["overall"])
# except ResponseError as error:
#     print("error")
#     print(error)