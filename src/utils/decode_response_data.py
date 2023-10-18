import json
def decode_response_data(response_data):
    json_data = json.dumps(response_data)
    decoded_data = json_data.encode("utf-8").decode("unicode-escape")
    decoded_data = decoded_data.replace('"', "'")

    return decoded_data