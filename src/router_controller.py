from responseFormatters import prepare_response_text, prepare_response_elicitSlot

def handlerLexIntentVerifier(event, context):
    intent = event['sessionState']['intent']['name']

    if (intent == 'ImageTextExtractionIntent'):
        imgFromUser            = event['sessionState']['intent']['slots']['imgFromUser']
        textOrAudioConditional = event['sessionState']['intent']['slots']['textOrAudioConditional']

        print(f'imgFromUser: {imgFromUser}')
        print(f'textOrAudioConditional: {textOrAudioConditional}')

        if (imgFromUser != None):
            print("entrou no if imgFromUser != None e vai ilicitar o slot textOrAudioConditional")
            return prepare_response_elicitSlot(event)
        
        if (textOrAudioConditional != None):
            if (textOrAudioConditional['value']['originalValue'] == 'text_fr'):
                return prepare_response_text(event, "imageTextExtraction concluida, usuario receberá texto em francês")
            if (textOrAudioConditional['value']['originalValue'] == 'audio_fr'):
                return prepare_response_text(event, "imageTextExtraction concluida, usuario receberá audio em francês")
            if (textOrAudioConditional['value']['originalValue'] == 'text_pt'):
                return prepare_response_text(event, "imageTextExtraction concluida, usuario receberá texto em portugues")
            if (textOrAudioConditional['value']['originalValue'] == 'audio_pt'):
                return prepare_response_text(event, "imageTextExtraction concluida, usuario receberá audio em portugues")
          
        return prepare_response_elicitSlot(event)

    elif (intent == 'TextAudioTranslater'):
        languageConditional    = event['sessionState']['intent']['slots']['languageConditional']
        textOrAudioReceiver    = event['sessionState']['intent']['slots']['textOrAudioReceiver']
        textOrAudioConditional = event['sessionState']['intent']['slots']['textOrAudioConditional']

        if (languageConditional != None):
            print("entrou no if languageConditional != None e vai ilicitar o slot textOrAudioReceiver")
            return prepare_response_elicitSlot(event)
        
        if (textOrAudioReceiver != None):
            print("entrou no if textOrAudioReceiver != None e vai ilicitar o slot textOrAudioConditional")
            return prepare_response_elicitSlot(event)
        
        if (textOrAudioConditional != None):
            if (textOrAudioConditional['value']['originalValue'] == 'text'):
                return prepare_response_text(event, "textAudioTranslater concluida, usuario receberá texto")
            if (textOrAudioConditional['value']['originalValue'] == 'audio'):
                return prepare_response_text(event, "textAudioTranslater concluida, usuario receberá audio")
            
        return prepare_response_elicitSlot(event)
    
    elif (intent == 'CepToTip'):
        cepFromUser      = event['sessionState']['intent']['slots']['cepFromUser']
        pointsOfInterest = event['sessionState']['intent']['slots']['pointsOfInterest']

        if (cepFromUser != None):
            print("entrou no if cepFromUser != None e vai ilicitar o slot pointsOfInterest")
            return prepare_response_elicitSlot(event)
        
        if (pointsOfInterest != None):
            if (pointsOfInterest['value']['originalValue'] == 'hospital'):
                return prepare_response_text(event, "cepToTip concluida, usuario receberá hospital")
            if (pointsOfInterest['value']['originalValue'] == 'policia'):
                return prepare_response_text(event, "cepToTip concluida, usuario receberá policia")
            if (pointsOfInterest['value']['originalValue'] == 'restaurante'):
                return prepare_response_text(event, "cepToTip concluida, usuario receberá restaurante")
            
        return prepare_response_elicitSlot(event)

    elif (intent == 'EmergencyContacts'):
        emergencyContact = event['sessionState']['intent']['slots']['emergencyContact']

        if (emergencyContact != None):
            if (emergencyContact['value']['originalValue'] == 'ambulancia'):
                return prepare_response_text(event, "emergencyContacts concluida, usuario receberá ambulancia")
            if (emergencyContact['value']['originalValue'] == 'policia'):
                return prepare_response_text(event, "emergencyContacts concluida, usuario receberá policia")
            if (emergencyContact['value']['originalValue'] == 'bombeiros'):
                return prepare_response_text(event, "emergencyContacts concluida, usuario receberá bombeiros")
            
        return prepare_response_elicitSlot(event)
    
    elif (intent == 'HowToMakeDocs'):
        return prepare_response_text(event, "eu entrei na intent HowToMakeDocs retorno")