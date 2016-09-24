import boto3
import json

from datetime import datetime

dynamo = boto3.resource('dynamodb').Table('tweets')

# ------------------------------------------------------------------------------
# Timestamp setting functions
# ------------------------------------------------------------------------------
def getCurrentUTCTime():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def setTimestamp(document):
    timestamp = getCurrentUTCTime()
    document['created_at'] = timestamp
    document['updated_at'] = timestamp
    return document

# ------------------------------------------------------------------------------
# DynamoDB handling functions
# ------------------------------------------------------------------------------
def createItem(document):
    document = setTimestamp(document)
    return dynamo.put_item(Item=document)

# ------------------------------------------------------------------------------
# Request handling functions
# ------------------------------------------------------------------------------
def respond(status_code, response):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': response
    }

def handlePOSTRequest(body):
    createItem(body)
    return respond('200', {
        'message': 'Success',
        'data': body
    })

def handleUnknownRequest():
    return respond('400', {
        'message': 'Unauthorized',
        'data': {}
    })

# ------------------------------------------------------------------------------
# Lambda event handler
# ------------------------------------------------------------------------------
def handler(event, context):
    method = event['httpMethod']

    # if method == 'GET':
        # payload = event['queryStringParameters']
    if method == 'POST':
        return handlePOSTRequest(json.loads(event['body']))
    else:
        return handleUnknownRequest()
