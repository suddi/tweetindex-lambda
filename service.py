import boto3
import json

from datetime import datetime

dynamo = boto3.resource('dynamodb').Table('tweets')

def getCurrentUTCTime():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def setTimestamp(document):
    timestamp = getCurrentUTCTime()
    document['created_at'] = timestamp
    document['updated_at'] = timestamp
    return document

def createItem(document):
    document = setTimestamp(document)
    return dynamo.put_item(Item=document)

def respond(status_code, response):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': response
    }

def handler(event, context):
    method = event['httpMethod']

    # if method == 'GET':
        # payload = event['queryStringParameters']
    if method == 'POST':
        body = json.loads(event['body'])
        createItem(body)
        return respond('200', {
            'message': 'Success',
            'data': body
        })
    else:
        return respond('400', {
            'message': 'Unauthorized',
            'data': {}
        })
