def prepare_response_text(event, msgText):
  """
  Prepares a response to be sent to Amazon lex
  
  @param event - The event that triggered the close intent
  @param msgText - The message text to send to Amazon lex
  
  @return - A dictionary that can be sent to Amazon lex with the close intent and the message text as
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
  Elicits an slot from an intent

  @param event - Evento recebido pelo lambda
  @param resultado - Texto a ser enviado para o usuário

  @return - JSON
  """

  slots        = []
  slotToElicit = ""

  for slot in event['sessionState']['intent']['slots']:
    # print(f"um dos slots da intent: {slot}")
    # print(f"valor do slot {slot}: {event['sessionState']['intent']['slots'][slot]}")

    slotAndValue = {
      "slot" : slot,
      "value": event['sessionState']['intent']['slots'][slot]
    }

    slots.append(slotAndValue)
  
  # print(slots)

  if (event['sessionState']['intent']['name'] == 'CepToTip'):
    slots.reverse()

  for slot in range (len(slots) -1, -1, -1):
    # print(f"valor do slot: {slot}")
    # print(f"posição do slots[slot]: {slots[slot]}")
    # print("slot value", slots[slot]['value'])

    if 'value' in slots[slot] and slots[slot]['value'] is not None:
      slotToElicit = slots[slot - 1]['slot']
      # print(f"slotToElicit: {slotToElicit}")
      break
    elif (slot == 0):
      slotToElicit = slots[len(slots) - 1]['slot']
      # print(f"slotToElicit: {slotToElicit}")
      break

  response = {
    "sessionState": {
      "dialogAction": {
          "slotToElicit": slotToElicit,
            "type": "ElicitSlot"
      },
      "intent": {
        "name": event['sessionState']['intent']['name'],
        "state": "Fulfilled"
      }
    }
  }

  return response