import requests
from utils.formatter import create_response_data
import base64
import urllib.parse
from core.config import settings

def orchestrator_handler(event, context):
  try:
    
    TWILIO_ID = settings.TWILIO_ID
    TWILIO_TOKEN = settings.TWILIO_TOKEN

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
          print("Received message media_url0:", media_url0)
          print("access_media_url:", access_media_url)
          download_image(access_media_url)

      else:
        body = query_dict.get('Body', [])[0]
        print("Received message body:", body)
    return create_response_data(200, 'Okay!!!')
  except Exception as e:
    print(f"An error occurred: {e}")
    return create_response_data(500, 'Internal Server Error')


def download_image(url):
  try:
    # Download the image from the given URL
    response = requests.get(url)
    print("Response Media: ", response)
  except Exception as e:
    print(f"An error occurred download Image: {e}")

