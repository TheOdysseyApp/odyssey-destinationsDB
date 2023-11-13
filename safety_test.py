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
    amadeus_client = create_amadeus_client()
    multiple_city = ["Muscat", "Rio de Janeiro", "Brussels", "Lisbon", "Paris"] # these cities return multiple city safety scores b/c search radius is too large
    no_city = ["Hong Kong", "Jerusalem", "Bangkok"] # these cities do not return an overall general city safety score only city district scores

    try:
        response = client.scan(TableName=table_name)
        if 'Items' in response:
            items = response['Items']
            # Process each item
            for item in items:
                city = item["city"]["S"]
                latitude = item["latitude"]["N"]
                longitude = item["longitude"]["N"]
                try:
                    response = amadeus_client.safety.safety_rated_locations.get(longitude=longitude, latitude=latitude, radius=7)
                    if city in no_city:
                        num = len(response.data)
                        safety_scores = {"lgbtq":0, 
                                        "medical":0, 
                                        "overall":0, 
                                        "physicalHarm":0, 
                                        "politicalFreedom":0, 
                                        "theft":0, 
                                        "women":0}
                        for data in response.data:
                            safety_scores["lgbtq"] += data["safetyScores"]["lgbtq"]
                            safety_scores["medical"] += data["safetyScores"]["medical"]
                            safety_scores["overall"] += data["safetyScores"]["overall"]
                            safety_scores["physicalHarm"] += data["safetyScores"]["physicalHarm"]
                            safety_scores["politicalFreedom"] += data["safetyScores"]["politicalFreedom"]
                            safety_scores["theft"] += data["safetyScores"]["theft"]
                            safety_scores["women"] += data["safetyScores"]["women"]
                        safety_scores["lgbtq"] //= num
                        safety_scores["medical"] //= num
                        safety_scores["overall"] //= num
                        safety_scores["physicalHarm"] //= num
                        safety_scores["politicalFreedom"] //= num
                        safety_scores["theft"] //= num
                        safety_scores["women"] //= num
                    else:
                        for data in response.data:
                            if data["subType"] == "CITY":
                                if city in multiple_city:
                                    if city == data["name"]:
                                        safety_scores = data["safetyScores"]
                                else:
                                    safety_scores = data["safetyScores"]
                                    break
                    safety_data = {"M": {"lgbtq":{"N":str(safety_scores["lgbtq"])}, 
                                        "medical":{"N":str(safety_scores["medical"])}, 
                                        "overall":{"N":str(safety_scores["overall"])}, 
                                        "physical_harm":{"N":str(safety_scores["physicalHarm"])}, 
                                        "political_freedom":{"N":str(safety_scores["politicalFreedom"])}, 
                                        "theft":{"N":str(safety_scores["theft"])}, 
                                        "women":{"N":str(safety_scores["women"])}}
                                }
                    try:
                        response = client.update_item(
                            TableName="travel-destination",
                            Key={"city": {"S": str(city)}},
                            UpdateExpression="set #safety = :safety",
                            ExpressionAttributeNames={
                                "#safety": "safety",
                            },
                            ExpressionAttributeValues={
                                ":safety": safety_data
                            },
                            ReturnValues="UPDATED_NEW",
                        )
                    except Exception as e:
                        print(f"Error: {e}")
                except ResponseError as error:
                    print(error)
                    print(f'Couldn\'t update safety of {city}')
                except Exception as e:
                    print(e)
                    print(f'Couldn\'t update safety of {city}')


        else:
            print("No items found in the table.")
    except Exception as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    # check if current file is the running file
    main()