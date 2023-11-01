import boto3
import csv

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('travel-destination')

def batch_write(items):
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

items = []
with open('../data/initial.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  
    for row in reader:
        city, country = row
        items.append({
            'city': city.strip(),
            'country': country.strip()
        })
        if len(items) == 25:  
            batch_write(items)
            items.clear()

if items:
    batch_write(items)

print("Data populated successfully!")