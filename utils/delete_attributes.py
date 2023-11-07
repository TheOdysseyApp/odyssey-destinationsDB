import boto3

dynamodb = boto3.resource('dynamodb')

table_name = 'travel-destination'

table = dynamodb.Table(table_name)

def remove_attributes(city_name):
    try:
        response = table.update_item(
            Key={
                'city': city_name  
            },
            UpdateExpression="REMOVE bike_score, walk_score, transit_score"
        )
        print(f"Attributes removed for {city_name}: {response}")
    except Exception as e:
        print(f"Error updating {city_name}: {e}")

def remove_attributes_from_all():
    paginator = dynamodb.meta.client.get_paginator('scan')

    for page in paginator.paginate(TableName=table_name):
        for item in page['Items']:
            city_name = item['city']
            remove_attributes(city_name)

remove_attributes_from_all()
