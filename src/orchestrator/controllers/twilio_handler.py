from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from core.config import settings
from utils.twilio_send_message import twilio_send_message

import boto3
s3 = boto3.client('s3')

TWILIO_WHATS_FROM = settings.TWILIO_WHATS_FROM
TWILIO_WHATS_TO = settings.TWILIO_WHATS_TO
TWILIO_ID = settings.TWILIO_ID
TWILIO_TOKEN = settings.TWILIO_TOKEN
BUCKET_NAME = settings.BUCKET_NAME

print(TWILIO_WHATS_FROM, TWILIO_WHATS_TO)

def twilio_handler(event, context):

    twilio_send_message("MENSAGEM DE TESTE DO HANDLER")
    
    return {
        "statusCode": 200,
        "body": "ok",
    }
