def lambda_handler(event, context):
    import boto3
    import json
    from decimal import Decimal
    from boto3.dynamodb.conditions import Key, Attr
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('#finaltablename')
    response = table.scan()
    hi=response['Items']
    return hi
    