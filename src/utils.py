def prepare_response_text(event, msgText):
  """
   Prepares a response to be sent to Amazon lex
   
   @param event - The event that triggered the close intent
   @param msgText - The message text to send to Amazon lex
   
   @return A dictionary that can be sent to Amazon lex with the close intent and the message text as
  """
  response = {
          "sessionState": {
            "dialogAction": {
              "type": "Close"
            },
            "intent": {
              "name": event['sessionState']['intent']['name'],
              "slots": event['sessionState']['intent']['slots'],
              "state": "Fulfilled"
            }
          },
          "messages": [
            {
              "contentType": "PlainText",
              "content": msgText
            }
            ]
        }
      
  return response