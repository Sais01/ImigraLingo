import base64
import urllib.parse


def decode_message(msg_data):
    
    decoded_data = base64.b64decode(msg_data)
    decoded_parsed_data = urllib.parse.parse_qs(decoded_data.decode('utf-8'))

    return decoded_parsed_data