import json
from utils.twilio_send_message import twilio_send_message
from twilio.twiml.messaging_response import MessagingResponse
import requests

from twilio.request_validator import RequestValidator
from requests.auth import HTTPDigestAuth
import requests
import urllib
import os

from core.config import settings

TWILIO_TOKEN = settings.TWILIO_TOKEN


def new_func_twilio(event, context):

    try:
        twilio_send_message("new func twilio test!!")


        # Get the request data
        print(event)
        print(event['headers'])
        request_data = event['body']
        request_signature = event['headers']['x-twilio-signature']
        print(request_signature)

        # Initialize the Twilio request validator
        validator = RequestValidator(TWILIO_TOKEN)

        # Validate the request using the Twilio request validator
        is_valid = validator.validate(request_signature, request_data, event['headers']['Host'])

        if is_valid:
            # The request is valid, process it
            # Parse the incoming WhatsApp message and respond accordingly
            # Add your logic here
            request_body = event['body']
            print(f"Incoming WhatsApp Message Body: {request_body}")

            return {
                'statusCode': 200,
                'body': 'Webhook received and validated.'
            }
        else:
            # The request is not valid; reject it
            return {
                'statusCode': 403,
                'body': 'Invalid request signature.'
            }

    except Exception as e:
        print(f"PRINT DE ERRO: {e}")

    return {
        'statusCode': 200,
        'body': "json.dumps(response)"
    }



import os
from twilio.request_validator import RequestValidator

def webhook(event, context):
    # Get the request data
    request_data = event['body']
    request_signature = event['headers']['X-Twilio-Signature']

    # Initialize the Twilio request validator
    validator = RequestValidator(os.environ['TWILIO_AUTH_TOKEN'])

    # Validate the request using the Twilio request validator
    is_valid = validator.validate(request_signature, request_data, event['headers']['Host'])

    if is_valid:
        # The request is valid, process it
        # Parse the incoming WhatsApp message and respond accordingly
        # Add your logic here

        return {
            'statusCode': 200,
            'body': 'Webhook received and validated.'
        }
    else:
        # The request is not valid; reject it
        return {
            'statusCode': 403,
            'body': 'Invalid request signature.'
        }
