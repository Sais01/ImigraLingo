from twilio.twiml.messaging_response import MessagingResponse
from core.config import settings

import boto3

# Initialize the S3 client
s3 = boto3.client('s3')

TWILIO_WHATS_FROM = settings.TWILIO_WHATS_FROM
TWILIO_WHATS_TO = settings.TWILIO_WHATS_TO

def twilio_send_message(text_message, client, TWILIO_WHATS_FROM=TWILIO_WHATS_FROM, TWILIO_WHATS_TO=TWILIO_WHATS_TO):

    if text_message.find("bucket.s3.amazonaws.com") != -1:
        message = client.messages.create(
            from_=TWILIO_WHATS_FROM,
            media_url=[text_message],
            to=TWILIO_WHATS_TO,
        )
    else:
        message = client.messages.create(
            from_=TWILIO_WHATS_FROM,
            body=text_message,
            to=TWILIO_WHATS_TO,
        )

    print(message)
    # If it's a text message, you can respond accordingly
    response = MessagingResponse()
    response.message("Received your text message. Thank you!")


    return response
