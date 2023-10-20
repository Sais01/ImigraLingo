from utils.response_formatters import prepare_response_text, prepare_response_elicitSlot
import boto3
import json


def handlerLexIntentVerifier(event, context):
    client = boto3.client('lambda')

    intent = event['sessionState']['intent']['name']

    if (intent == 'IntroductionIntent'):
        response = f"Boas vindas ao ImigraLingo, bot de ajuda ao imigrante! O que deseja fazer? Caso não conheça meus comandos, digite 'ajuda'!"
        return prepare_response_text(event, response)
    
    elif (intent == 'ImageTextExtractionIntent'):
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

    elif (intent == 'TextAudioTranslaterIntent'):
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
    
    elif (intent == 'CepToTipIntent'):
        invoke_response = client.invoke(FunctionName="final-lex-bot-v1-dev-cep_to_places", Payload = json.dumps(event))
        print(invoke_response)
        payload = json.load(invoke_response['Payload'])
        return payload

    elif (intent == 'EmergencyContactsIntent'):
        emergencyContact = event['sessionState']['intent']['slots']['emergencyContact']

        if (emergencyContact != None):
            if (emergencyContact['value']['originalValue'] == 'ambulancia'):
                return prepare_response_text(event, "emergencyContacts concluida, usuario receberá ambulancia")
            if (emergencyContact['value']['originalValue'] == 'policia'):
                return prepare_response_text(event, "emergencyContacts concluida, usuario receberá policia")
            if (emergencyContact['value']['originalValue'] == 'bombeiros'):
                return prepare_response_text(event, "emergencyContacts concluida, usuario receberá bombeiros")
            
        return prepare_response_elicitSlot(event)
    
    elif (intent == 'HowToMakeDocsIntent'):
        link     = "https://encurtador.com.br/nqswz"
        response = f"Você pode encontrar todas as informações necessárias para a emissão de documentos no link: {link}"
        return prepare_response_text(event, response)