import csv
import sys
import json
from typing import Dict, List

def parse_csv(file:str)->List[Dict]:
    '''
    parses the csv file and returns it as a list of dictionaries
    '''
    results = []
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            results.append(row)
    return results

def json_dump(file:str, parsed:List[Dict]):
    '''
    dumps a list of dictionaries into a json file
    '''
    with open(file, 'w') as file:
        json.dump(parsed, file)

if __name__ == "__main__":
    # first arg is csv file to be parsed
    # second arg is json file that results will be written to
    json_dump(sys.argv[2], parse_csv(sys.argv[1]))
