import os
import pandas as pd
from data_collector.collector import DataCollector
from db.DynamoClient import create_client
from utils.types import DATA_MAP
from data_collector.AmadeusClient import create_amadeus_client
from amadeus import ResponseError


def main():

    client = create_client(service_name="dynamodb", region_name="us-east-1")
    table_name = "travel-destination"

    try:
        response = client.scan(TableName=table_name)
        if 'Items' in response:
            items = response['Items']
            # Process each item
            for item in items:
                print(f"{item}")
        else:
            print("No items found in the table.")
    except Exception as e:
        print(f"Error: {e}")

    # item structure -> { "name_of_attribute": { "data_type": data_value } }
    
    amadeus_client = create_amadeus_client()
    try:
        response = amadeus_client.safety.safety_rated_locations.get(longitude=2.160873, latitude=41.397158)
        city_name = response.data[0]["name"]
        safety_scores = response.data[0]["safetyScores"]
        # print(response.data[0]["name"])
        # print(response.data[0]["safetyScores"])
        # print(response.data[0]["safetyScores"]["overall"])
        item_data = {
            "city": {"S": city_name},
            "country": {"S": "Spain"},
            "safety": {"M": {"lgbtq":{"N":str(safety_scores["lgbtq"])}, "medical":{"N":str(safety_scores["medical"])}, 
                             "overall":{"N":str(safety_scores["overall"])}, "physical_harm":{"N":str(safety_scores["physicalHarm"])}, 
                             "political_freedom":{"N":str(safety_scores["politicalFreedom"])}, 
                             "theft":{"N":str(safety_scores["theft"])}, "women":{"N":str(safety_scores["women"])}}}
        }
        try:
            client.put_item(
                TableName=table_name,
                Item={k: v for k, v in item_data.items()}
            )
            print("Item created successfully.")
        except Exception as e:
            print(f"Error: {e}")
    except ResponseError as error:
        print(error)

    try:
        response = client.update_item(
            TableName="travel-destination",
            Key={"city": {"S": "Barcelona"}},
            UpdateExpression="set #lat = :lat, #long = :long",
            ExpressionAttributeNames={
                "#lat": "latitude",
                "#long": "longitude",
            },
            ExpressionAttributeValues={
                ":lat": {"N": "41.397158"},
                ":long": {"N": "2.160873"},
            },
            ReturnValues="UPDATED_NEW",
        )
        print("Items updated successfully")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # check if current file is the running file
    main()