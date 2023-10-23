import os
import json
import requests
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from typing import Dict, List, Tuple, Any

load_dotenv()

class DataCollector():
    def __init__(self, read_dir: str, output_dir: str, url_json: str):
        self.output_dir = output_dir
        with open(os.path.join(read_dir, f'{url_json}.json'), 'r') as file:
            self.urls = json.load(file)

    def _get_countries(self) -> List[str]:
        LIVING_COST_API_KEY = os.getenv("LIVING_COST_API_KEY")
        url = self.urls["get-countries"]
        headers = {
            'Authorization': f'Bearer {LIVING_COST_API_KEY}'
        }
        response = requests.request("GET", url, headers=headers)
        if response == None:
            return []

        data = json.loads(response.text)
        countries = ["" for _ in range(len(data))]
        for i in range(len(data)):
            countries[i] = data[i]["country"]
        return countries

    def _get_cities(self, country: str) -> List[str]:
        LIVING_COST_API_KEY = os.getenv("LIVING_COST_API_KEY")
        url = self.urls["get-cities"]
        query = f"country={country}"
        headers = {
            'Authorization': f'Bearer {LIVING_COST_API_KEY}'
        }
        response = requests.request("GET", url+query, headers=headers)
        if response == None:
            return []

        data = json.loads(response.text)
        cities = np.empty(len(data), dtype=str)
        cities = ["" for _ in range(len(data))]
        for i in range(len(data)):
            cities[i] = data[i]["city"]
        return cities

    def _get_one_city_cost(self, country: str, city: str) -> Dict:
        LIVING_COST_API_KEY = os.getenv("LIVING_COST_API_KEY")
        url = self.urls["cost"]
        query = f"country={country}&city={city}"
        headers = {
            'Authorization': f'Bearer {LIVING_COST_API_KEY}'
        }
        response = requests.request("GET", url+query, headers=headers)
        if response == None:
            return {}
        
        response_dict = json.loads(response.text)
        return {
            "amount": response_dict["Cost of Living Month Total"],
            "currency": response_dict["Currency"]
        }

    def collect_cost_information(self, cities_info: List[Tuple[str, str]]) -> List[Dict]:
        cost_info = np.empty(len(cities_info), dtype=object)
        for i in range(len(cities_info)):
            city_info = cities_info[i]
            cost_info[i] = self._get_one_city_cost(country=city_info[0], city=city_info[1])
        return cost_info.tolist()

