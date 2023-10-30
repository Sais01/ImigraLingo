import json

def create_response_data(statusCode, body):
    """
     Create response data to send to API.
     
     @param statusCode - status code of the response
     @param body - JSON - encoded body of the response. It is assumed that the content type is application / json
     
     @return dict with response data in JSON format.
    """
    return {
        'statusCode': statusCode,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        'body': json.dumps(body),
    }