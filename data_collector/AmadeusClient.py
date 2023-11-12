from amadeus import Client, ResponseError
from dotenv import load_dotenv
import os

load_dotenv()

def create_amadeus_client():
    amadeus = Client(
        client_id=os.getenv("AMADEUS_PROD_KEY"),
        client_secret=os.getenv("AMADEUS_PROD_SECRET"),
        hostname="production"
    )
    return amadeus

# if __name__ == "__main__":
#     amadeus = create_amadeus_client()
#     try:
#         response = amadeus.safety.safety_rated_locations.get(longitude=72.878176, latitude=19.0785451, radius=5)
#         # response = amadeus.safety.safety_rated_locations.get(longitude=2.160873, latitude=41.397158)
#         print("test")
#         print(response.data)
#         # print(response.data[0]["name"])
#         # print(response.data[0]["safetyScores"])
#         # print(response.data[0]["safetyScores"]["overall"])
#     except ResponseError as error:
#         print("error")
#         print(error)