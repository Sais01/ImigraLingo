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

def prepare_response_elicitSlot(event):
    """
    Elicita o slot da intent

    :param event: Evento recebido pelo lambda
    :param resultado: Texto a ser enviado para o usuário
    :return: JSON
    """

    # prepara a resposta final do bot
    response = {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": "DadoAluno",
                "type": "ElicitSlot"
            },
            "intent": {
                "name": event['sessionState']['intent']['name'],
                "state": "Fulfilled"
            }
        }
       }

    return response