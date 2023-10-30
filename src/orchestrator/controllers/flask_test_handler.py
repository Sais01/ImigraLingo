from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json


app = Flask(__name__)


GOOD_BOY_URL = (
    "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?ixlib=rb-1.2.1"
    "&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"
)


@app.route("/whatsapp", methods=["GET", "POST"])
def reply_whatsapp():

    try:
        num_media = int(request.values.get("NumMedia"))
    except (ValueError, TypeError):
        return "Invalid request: invalid or missing NumMedia parameter", 400
    response = MessagingResponse()
    if not num_media:
        msg = response.message("Send us an image!")
    else:
        msg = response.message("Thanks for the image. Here's one for you!")
        msg.media(GOOD_BOY_URL)
    return str(response)

def flask_test_handler(event, context):
    print("$$$$$$$$$$$$$$$$$$")
    print(event)
    print(event["path"])
    # Create a response dictionary
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/plain"
        },
        "body": "This is a default response"
    }
    
    # Use the Flask app to handle the request
    with app.test_request_context(event["path"], method=event["httpMethod"]):
        try:
            response_body = app.full_dispatch_request()
            response["statusCode"] = response_body.status_code
            response["body"] = response_body.data
        except Exception as e:
            response["statusCode"] = 500
            response["body"] = f"An error occurred: {str(e)}"
    
    return response