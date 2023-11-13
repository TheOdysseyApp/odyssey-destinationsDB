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