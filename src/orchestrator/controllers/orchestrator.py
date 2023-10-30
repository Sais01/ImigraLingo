from utils.formatter import create_response_data
import base64
import urllib.parse
from core.config import settings
from services.s3 import upload_s3

def orchestrator_handler(event, context):
  try:
    
    TWILIO_ID = settings.TWILIO_ID
    TWILIO_TOKEN = settings.TWILIO_TOKEN

    BUCKET_NAME = settings.BUCKET_NAME

    if 'body' in event:
      message = event['body']

      message = base64.b64decode(message)
      print("Received message body:", (message))

      # Parse the query string into a dictionary
      query_dict = urllib.parse.parse_qs(message.decode('utf-8'))

      profile_name = query_dict.get('ProfileName', [])[0]
      print("Received message profile_name:", profile_name)

      whatsapp_number = query_dict.get('WaId', [])[0]
      print("Received message whatsapp_number:", whatsapp_number)

      whatsapp_from = query_dict.get('From', [])[0]
      print("Received message whatsapp_from:", whatsapp_from)

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

      else:
        body = query_dict.get('Body', [])[0]
        print("Received message body:", body)
    
    return create_response_data(200, 'Okay!!!')
  except Exception as e:
    print(f"An error occurred: {e}")
    return create_response_data(500, 'Internal Server Error')


