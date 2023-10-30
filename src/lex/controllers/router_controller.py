import boto3
import json
import os

# reuse client connection as global
client = boto3.client('lambda')

def handle_lex_intent_verifier(event, context):
    """
    This function handles the routing of incoming requests to the appropriate AWS Lambda function based on the intent name.
    It first extracts the intent name from the incoming event, then looks up the corresponding Lambda function name from an environment variable.
    If a function name is found, it invokes the Lambda function with the incoming event as the payload and returns the response.
    If no function name is found, it raises an exception.

    Args:
        event (dict): The incoming event object containing the session state and intent information.
        context (object): The AWS Lambda context object.

    Returns:
        dict: The response payload from the invoked Lambda function.

    Raises:
        Exception: If no environment variable is found for the intent name.
    """
    intent_name = event['sessionState']['intent']['name']
    fn_name     = os.environ.get(intent_name)
    print(f"Intent: {intent_name} -> Lambda: {fn_name}")
    print("VERIFIER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(event)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!VERIFIER")

    if (fn_name):
        invoke_response = client.invoke(FunctionName=fn_name, Payload = json.dumps(event))
        print(invoke_response)
        payload = json.load(invoke_response['Payload'])

        return payload
    
    raise Exception('No environment variable for intent: ' + intent_name)