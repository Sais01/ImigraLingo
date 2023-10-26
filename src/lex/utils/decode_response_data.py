import json

def decode_response_data(phrase):
  """
  Decodes a given phrase and returns it as a JSON object.

  Args:
    phrase (str): The phrase to be decoded.

  Returns:
    dict: A dictionary containing the status code and the decoded phrase as a JSON object.
  """
  try:
    json_str = json.dumps({"phrase": phrase})
    decoded_str = json_str.encode("utf-8").decode("unicode-escape")
    json_data = json.loads(decoded_str)

    return {"statusCode": 200, "body": json_data}

  except Exception as e:
    print(f"Error decode response util: {e}")

    # return {"statusCode": 404, "body": "ERROR"}