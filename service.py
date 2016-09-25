# -*- coding: utf-8 -*-

import boto3
import json

from datetime import datetime

tweet = boto3.resource('dynamodb').Table('tweets')
error = boto3.resource('dynamodb').Table('errors')

# ------------------------------------------------------------------------------
# Timestamp setting functions
# ------------------------------------------------------------------------------
def get_current_time():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def set_timestamp(document):
    timestamp = get_current_time()
    document['created_at'] = timestamp
    document['updated_at'] = timestamp
    return document

# ------------------------------------------------------------------------------
# DynamoDB handling functions
# ------------------------------------------------------------------------------
def create_item(document):
    # document = set_timestamp(document)
    if document['type'] == 'tweet':
        return tweet.put_item(Item=document)
    else:
        return error.put_item(Item=document)

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

def handle_post_request(body):
    create_item(body)
    return respond('200', {
        'message': 'OK',
        'data': body
    })

def handle_unknown_request():
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
        return handle_post_request(json.loads(event['body']))
    else:
        return handle_unknown_request()
