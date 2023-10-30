import boto3
import json

from twilio.rest import Client
from core.config import settings
from utils.twilio_send_message import twilio_send_message
from orchestrator.utils.decode_message import twilio_get_message

# Initialize the S3 client
s3 = boto3.client('s3')
lex_bot = boto3.client('lexv2-runtime', region_name='us-east-1')

TWILIO_WHATS_FROM = settings.TWILIO_WHATS_FROM
TWILIO_WHATS_TO = settings.TWILIO_WHATS_TO
TWILIO_ID = settings.TWILIO_ID
TWILIO_TOKEN = settings.TWILIO_TOKEN
BOT_ID = settings.BOT_ID
BOT_ALIAS = settings.BOT_ALIAS


def new_func_twilio(event, context):

    try:
        client = Client(TWILIO_ID, TWILIO_TOKEN)

        twilio_send_message("Testando orquestrador", client)
        
        msg_received = event['body']
        msg_data = twilio_get_message(msg_received)
        print("ççççç")

        print("------------------------------------")
        print(msg_data)

        profile_name = msg_data.get('ProfileName', [])[0]
        print("Received message profile_name:", profile_name)

        whatsapp_number = msg_data.get('WaId', [])[0]
        print("Received message whatsapp_number:", whatsapp_number)

        whatsapp_from = msg_data.get('From', [])[0]
        print("Received message whatsapp_from:", whatsapp_from)

        num_media = msg_data.get('NumMedia', [])[0]
        print("Received message num_media:", num_media)

        msg_body = msg_data.get('Body', [])[0]
        print("Received message body:", msg_body)

        response = lex_bot.recognize_text(
            botId=BOT_ID,
            botAliasId=BOT_ALIAS,
            localeId='pt_BR',
            sessionId='1222222222223333333333355555',  # Você pode usar uma sessão existente ou criar uma nova
            text=msg_body
        )


    except Exception as e:
        print(f"PRINT DE ERRO: {e}")

    return {
        'statusCode': 200,
        'body': "json.dumps(response)"
    }


