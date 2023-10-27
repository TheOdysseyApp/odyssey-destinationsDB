import os
import pandas as pd
from data_collector.collector import DataCollector
from db.DynamoClient import create_client
from utils.types import DATA_MAP


def main():
    # collector = DataCollector(
    #     read_dir=os.getcwd(),
    #     output_dir=os.path.join(os.getcwd(), "data"),
    #     url_json="url"
    # )
    # df = pd.read_csv(os.path.join(os.getcwd(), "data", "cost.csv"))
    # # df = df.drop(df.columns[0], axis=1)
    # cities = df["city"].to_list()
    # cities_info = [('united-states', 'aberdeen-sd'), ('united-states', 'aberdeen-wa'), ('united-states', 'abilene-tx'), ('united-states', 'abingdon-md'), ('united-states', 'adelanto-ca')]
    # cost_info = collector.collect_cost_information(cities_info=cities_info)
    # df.loc[:4, 'monthly_cost_of_living'] = [f"{d['amount']} {d['currency']}" for d in cost_info]
    # print(df.loc[:4])
    # df.to_csv(os.path.join(os.getcwd(), "data", "cost.csv"), mode='w')
    # for city, cost in zip(cities, cost_info):
    #     print(f"{city}: {cost['amount']} {cost['currency']}")

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
    item_data = {
        "city": { DATA_MAP[type('irvine-ca')]: "irvine-ca" },
        "monthly_cost_of_living": {"S": "2000 USD"}
    }

    try:
        client.put_item(
            TableName=table_name,
            Item={k: v for k, v in item_data.items()}
        )
        print("Item created successfully.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # check if current file is the running file
    main()