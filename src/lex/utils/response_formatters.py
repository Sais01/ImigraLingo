def prepare_response_text(event, msgText):
  """
  Prepares a response object to be returned by the AWS Lex bot.

  Args:
  - event: dict containing the event data passed to the Lambda function by AWS Lex.
  - msgText: str containing the message text to be returned to the user.

  Returns:
  - response: dict containing the response object to be returned by the Lambda function to AWS Lex.
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
  Prepares a response to elicit a slot from the user during a Lex bot conversation.

  Args:
  - event: a dictionary containing the event data passed to the Lambda function by Amazon Lex.

  Returns:
  - A dictionary containing the response to elicit a slot from the user during a Lex bot conversation.
  """
  slots        = []
  slotToElicit = ""

  for slot in event['sessionState']['intent']['slots']:
    slotAndValue = {
      "slot" : slot,
      "value": event['sessionState']['intent']['slots'][slot]
    }

    slots.append(slotAndValue)

  if (event['sessionState']['intent']['name'] == 'CepToTip'):
    slots.reverse()

  for slot in range (len(slots) -1, -1, -1):

    if 'value' in slots[slot] and slots[slot]['value'] is not None:
      slotToElicit = slots[slot - 1]['slot']
      break
    elif (slot == 0):
      slotToElicit = slots[len(slots) - 1]['slot']
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