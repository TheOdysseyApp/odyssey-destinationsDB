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
                        safety_scores = response.data[0]["safetyScores"]
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


        else:
            print("No items found in the table.")
    except Exception as e:
        print(f"Error: {e}")


    #TESTING STUFF

    # item structure -> { "name_of_attribute": { "data_type": data_value } }
    
    # amadeus_client = create_amadeus_client()
    # try:
    #     response = amadeus_client.safety.safety_rated_locations.get(longitude=-117.82311, latitude=33.66946, radius=7)
    #     # city_name = response.data[0]["name"]
    #     for data in response.data:
    #         if data["subType"] == "CITY":
    #             safety_scores = data["safetyScores"]
    #             # print(safety_scores)
    #             break
    #     # safety_scores = response.data[0]["safetyScores"]
    #     safety_data = {"M": {"lgbtq":{"N":str(safety_scores["lgbtq"])}, 
    #                                     "medical":{"N":str(safety_scores["medical"])}, 
    #                                     "overall":{"N":str(safety_scores["overall"])}, 
    #                                     "physical_harm":{"N":str(safety_scores["physicalHarm"])}, 
    #                                     "political_freedom":{"N":str(safety_scores["politicalFreedom"])}, 
    #                                     "theft":{"N":str(safety_scores["theft"])}, 
    #                                     "women":{"N":str(safety_scores["women"])}}}
    #     # print(response.data[0]["name"])
    #     # print(response.data[0]["safetyScores"])
    #     # print(response.data[0]["safetyScores"]["overall"])
    #     # item_data = {
    #     #     "city": {"S": city_name},
    #     #     "country": {"S": "Spain"},
    #     #     "safety": {"M": {"lgbtq":{"N":str(safety_scores["lgbtq"])}, "medical":{"N":str(safety_scores["medical"])}, 
    #     #                      "overall":{"N":str(safety_scores["overall"])}, "physical_harm":{"N":str(safety_scores["physicalHarm"])}, 
    #     #                      "political_freedom":{"N":str(safety_scores["politicalFreedom"])}, 
    #     #                      "theft":{"N":str(safety_scores["theft"])}, "women":{"N":str(safety_scores["women"])}}}
    #     # }
    #     # try:
    #     #     client.put_item(
    #     #         TableName=table_name,
    #     #         Item={k: v for k, v in item_data.items()}
    #     #     )
    #     #     print("Item created successfully.")
    #     # except Exception as e:
    #     #     print(f"Error: {e}")
    # # except ResponseError as error:
    # #     print(error)

    # # try:
    #     response = client.update_item(
    #         TableName="travel-destination",
    #         Key={"city": {"S": "test_city"}}, 
    #         UpdateExpression="set #safety = :safety", 
    #         ExpressionAttributeNames={
    #             "#safety": "safety",
    #         },
    #         ExpressionAttributeValues={
    #             ":safety": safety_data
    #         },
    #         ReturnValues="UPDATED_NEW",
    #     )
    #     print("Items updated successfully")
    # except Exception as e:
    #     print(f"Error: {e}")


if __name__ == "__main__":
    # check if current file is the running file
    main()