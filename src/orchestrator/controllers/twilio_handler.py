import boto3
from core.config import settings
from utils.twilio_send_message import twilio_send_message

import os
from twilio.twiml.messaging_response import MessagingResponse
import json



s3 = boto3.client('s3')
client = boto3.client('lexv2-runtime', region_name='us-east-1')

TWILIO_WHATS_FROM = settings.TWILIO_WHATS_FROM
TWILIO_WHATS_TO = settings.TWILIO_WHATS_TO
TWILIO_ID = settings.TWILIO_ID
TWILIO_TOKEN = settings.TWILIO_TOKEN
BUCKET_NAME = settings.BUCKET_NAME
START_CONVERSATION_MESSAGE = settings.START_CONVERSATION_MESSAGE

text_message = "ola, teste com vs code"

def twilio_handler(event, context):
    

    print(event)
    print("EVENT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! EVENT")
    print(json.dumps(event['body']))
    print("2EVENT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! EVENT")
    twilio_send_message(text_message)

    # media_url = event['body']['MediaUrl0']
    # print("MEDIA URL @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print(media_url)
    # s3_bucket = BUCKET_NAME
    # s3_key = os.path.basename(media_url)

    # response = s3.put_object(
    #     Bucket=s3_bucket,
    #     Key=s3_key,
    #     Body=media_url,
    # )

    # twiml = MessagingResponse()
    # twiml.message("Image received and saved to S3")


    while True:
        # Solicitar a entrada do usuário
        user_input = input("Você: ")

        # Verificar se o usuário deseja encerrar o diálogo
        if user_input.lower() == 'sair':
            print("Encerrando o diálogo.")
            break
        
        response = client.recognize_text(
            botId='',
            botAliasId='',
            localeId='pt_BR',
            sessionId='TESTE',  # Você pode usar uma sessão existente ou criar uma nova
            text=user_input
        )

        # Obter a resposta do bot
        bot_response = response['messages'][0]['content']
        print("Bot: ",bot_response)


    return {
        'statusCode': 200,
        'body': "ok",
    }

    # return {
    #     "statusCode": 200,
    #     "body": "send_message_response",
    # }
