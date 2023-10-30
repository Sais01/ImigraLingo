import base64
import urllib.parse


def twilio_get_message(msg_data):
    
    decoded_data = base64.b64decode(msg_data)
    decoded_parsed_data = urllib.parse.parse_qs(decoded_data.decode('utf-8'))
    print('AQUI!!')
    print(decoded_parsed_data)

    return decoded_parsed_data