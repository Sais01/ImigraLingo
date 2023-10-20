import json


def decode_response_data(phrase):

    try:
        # json_data = json.dumps(response_data)
        json_str = json.dumps({"phrase": phrase})
        decoded_str = json_str.encode("utf-8").decode("unicode-escape")
        json_data = json.loads(decoded_str)

        # json_object = json.loads(json_string)


        return {"statusCode": 200, "body": json_data}

    except Exception as e:
        print(e)
        return {"statusCode": 404, "body": "ERROR"}
