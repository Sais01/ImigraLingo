from utils.formatter import create_response_data
from core.config import settings
from services.s3 import upload_s3
from services.lex import send_message_lex, get_session
from services.twilio import twilio_send_message
from twilio.rest import Client
from utils.decode_message import decode_message
from utils.numeric_menu import numeric_menu

def orchestrator_handler(event, context):
  try:
    
    TWILIO_ID = settings.TWILIO_ID
    TWILIO_TOKEN = settings.TWILIO_TOKEN
    client_twilio = Client(TWILIO_ID, TWILIO_TOKEN)

    BUCKET_NAME = settings.BUCKET_NAME

    BOT_ID = settings.BOT_ID
    BOT_ALIAS = settings.BOT_ALIAS

    if 'body' in event:
      
      message = event['body']
      query_dict = decode_message(message)

      #Session id
      whatsapp_number = query_dict.get('WaId', [])[0]
      print("Received message whatsapp_number:", whatsapp_number)

      whatsapp_from = query_dict.get('From', [])[0]
      print("Received message whatsapp_from:", whatsapp_from)

      whatsapp_to = query_dict.get('To', [])[0]
      print("Received message whatsapp_to:", whatsapp_to)

      num_media = query_dict.get('NumMedia', [])[0]
      print("Received message num_media:", num_media)

      if num_media != "0":
        media_url0 = query_dict.get('MediaUrl0', [])[0]
        if media_url0:
          access_media_url = media_url0.split("api", 1)
          access_media_url = f"{access_media_url[0]}{TWILIO_ID}:{TWILIO_TOKEN}@api{access_media_url[1]}"

          media_content_format = (query_dict.get('MediaContentType0', [])[0]).split("/")[1]

          print("Received message media_url0:", media_url0)
          print("access_media_url:", access_media_url)
          response_upload_s3 = upload_s3(BUCKET_NAME, access_media_url,media_content_format )
          print("response_upload_s3:", response_upload_s3)

          input_lex = response_upload_s3

      else:
        body = query_dict.get('Body', [])[0]
        print("Received message body:", body)
        message_lex = body

        response_lex_session = get_session(BOT_ID, BOT_ALIAS, whatsapp_number)

        if response_lex_session:
          print("response_lex_session:", response_lex_session)
        
          user_current_intent       = response_lex_session['sessionState']['intent']['name']

          try:
            user_current_slotToElicit = (response_lex_session['sessionState']['dialogAction']['slotToElicit'])
          except Exception as e:
            print(f"Error: {e}")
            user_current_slotToElicit = None

          input_lex = numeric_menu(user_current_intent, user_current_slotToElicit, message_lex)
        else:
          input_lex = message_lex

      response_message_lex = send_message_lex(input_lex, BOT_ID, BOT_ALIAS, whatsapp_number)

      twilio_send_message(response_message_lex, client_twilio, whatsapp_to, whatsapp_from)

    return create_response_data(200, 'Ok')
  except Exception as e:
    print(f"An error occurred: {e}")
    return create_response_data(500, 'Internal Server Error')


