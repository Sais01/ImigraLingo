from utils import prepare_response_text, prepare_response_elicitSlot

def handlerLexIntentVerifier(event, context):
    intent = event['sessionState']['intent']['name']

    if (intent == 'ImageTextExtractionIntent'):
        eventslots = event['sessionState']['intent']['slots']['DadoAluno']
        print('eventslots:',eventslots)
        if (eventslots != None):
            print('eventslots slot valor:',eventslots['value']['originalValue'])
            if (eventslots['value']['originalValue'] == '1'):
                return prepare_response_text(event, "eu entrei na intent ConsultarDadosAlunosIntent retorno prepareResponseRespostaFinal valor 1")
            if (eventslots['value']['originalValue'] == '2'):
                return prepare_response_text(event, "eu entrei na intent ConsultarDadosAlunosIntent retorno prepareResponseRespostaFinal valor 2")
        
        return prepare_response_elicitSlot(event)

    elif (intent == 'TextAudioTranslater'):
        return prepare_response_text(event, "eu entrei na intent TextAudioTranslater retorno")
    
    elif (intent == 'CepToTip'):
        return prepare_response_text(event, "eu entrei na intent CepToTip retorno")

    elif (intent == 'EmergencyContacts'):
        return prepare_response_text(event, "eu entrei na intent EmergencyContacts retorno")
    
    elif (intent == 'HowToMakeDocs'):
        return prepare_response_text(event, "eu entrei na intent HowToMakeDocs retorno")