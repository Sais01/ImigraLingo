import json


def decode_response_data(phrase):

    try:
        # json_data = json.dumps(response_data)
        json_data = json.dumps({"phrase": phrase}, indent=4)
        decoded_data = json_data.encode("utf-8").decode("unicode-escape")

        # json_object = json.loads(json_string)


        return {"statusCode": 200, "body": decoded_data}

    except Exception as e:
        print(e)
        return {"statusCode": 404, "body": "ERROR"}
