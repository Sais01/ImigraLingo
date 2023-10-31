import boto3

def send_message_lex(user_input, botId, botAliasId, sessionId):
  try:
    client = boto3.client('lexv2-runtime')

    response = client.recognize_text(
        botId=botId,
        botAliasId=botAliasId,
        localeId='pt_BR',
        sessionId=sessionId, 
        text=user_input
    )

    # Obter a resposta do bot
    
    bot_message = response['messages'][0]['content']
    return bot_message
  
  except Exception as e:
    print(f"Error: {e}")
    return None
  
def get_session(botId, botAliasId, sessionId):
  try:
    client = boto3.client('lexv2-runtime')
    response = client.get_session(
      botId=botId,
      botAliasId=botAliasId,
      localeId='pt_BR',
      sessionId=sessionId
    )

    return response
  
  except Exception as e:
    print(f"Error: {e}")
    return None