import boto3

def send_message_lex(user_input, botId, botAliasId, sessionId):
  
  client = boto3.client('lexv2-runtime')

  response = client.recognize_text(
      botId=botId,
      botAliasId=botAliasId,
      localeId='pt_BR',
      sessionId=sessionId, 
      text=user_input
  )

  # Obter a resposta do bot
  bot_response = response['messages'][0]['content']
  print("Bot: ", bot_response)
  return bot_response