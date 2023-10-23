import os
import pandas as pd
from data_collector.collector import DataCollector


def main():
    collector = DataCollector(
        read_dir=os.getcwd(),
        output_dir=os.path.join(os.getcwd(), "data"),
        url_json="url"
    )
    df = pd.read_csv(os.path.join(os.getcwd(), "data", "cost.csv"))
    cities = df["city"].to_list()
    cities_info = [(str("united-states"), city) for city in cities[:5]]
    cost_info = collector.collect_cost_information(cities_info=cities_info)
    # for city, cost in zip(cities, cost_info):
    #     print(f"{city}: {cost['amount']} {cost['currency']}")
    


if __name__ == "__main__":
    main()