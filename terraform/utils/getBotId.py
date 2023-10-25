import boto3
import json
import os

def get_bot_id():
    """
    Gets the bot id from the bot name at amazon lex

    @return A dictionary with the bot id
    """
    region = "us-east-1"
    bot_name = "finalSprintBot"
    lexv2_client = boto3.client('lexv2-models', region_name=region)

    try:
        response = lexv2_client.list_bots()
        for bot in response['botSummaries']:
            if bot['botName'] == bot_name:
                bot_id = bot['botId']
                return {"bot_id": f"{bot_id}"}
    except Exception as e:
        return {"error": str(e)}
    
print(json.dumps(get_bot_id()))