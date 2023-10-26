from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from core.config import settings

import boto3
# from io import BytesIO
# from PIL import Image
# import requests

# Initialize the S3 client
s3 = boto3.client('s3')

BUCKET_NAME = settings.BUCKET_NAME
TWILIO_WHATS_TO = settings.TWILIO_WHATS_TO



def get_twilio_message(event, context):

    body = event['Body']
    from_whatsapp_number = event['From']

    twilio_account_sid = "id"
    twilio_auth_token = "token"
    client = Client(twilio_account_sid, twilio_auth_token)

    # message = client.messages.create(
    #     from_="whatsapp:+14155238886",
    #     body="TESTANDO A MENSAGEM NO WHATS",
    #     to="whatsapp:+555391155927",
    # )

    print("1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(message.body)  # MENSAGEM PROPRIAMENTE DITA
    print("2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(message.sid)  # ID DE SESSÃO
    print("3!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    # Check if the message contains media
    # if 'MediaUrl0' in event:
    #     print("2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #     print('MEDIAURL0')  
    #     print("3!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #     media_url = event['MediaUrl0']

    #     # Download the image from the URL
    #     image_response = requests.get(media_url)
    #     if image_response.status_code == 200:
    #         image_data = image_response.content

    #         # Process the image (resize, crop, etc.) if needed
    #         # For example, resizing the image to a specific size using Pillow
    #         image = Image.open(BytesIO(image_data))
    #         image = image.resize((800, 600))

    #         # Upload the processed image to an S3 bucket
    #         bucket_name = 'mathspin-bot-sprint9e10'
    #         key = 'processed-image.jpg'

    #         s3.put_object(Bucket=bucket_name, Key=key, Body=image.tobytes())

    #         # Create a TwiML response to reply with a message
    #         response = MessagingResponse()
    #         response.message("Received your image and saved it to S3!")

    #         return {
    #             'statusCode': 200,
    #             'body': str(response),
    #         }

    # If it's a text message, you can respond accordingly
    response = MessagingResponse()
    response.message("Received your text message. Thank you!")

    return {
        "statusCode": 200,
        "body": str(response),
    }
