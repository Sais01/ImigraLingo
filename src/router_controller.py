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
        invoke_response = client.invoke(FunctionName="final-lex-bot-v1-dev-image_to_text", Payload = json.dumps(event))
        print(invoke_response)
        payload = json.load(invoke_response['Payload'])
        return payload


    elif (intent == 'TextAudioTranslaterIntent'):
        invoke_response = client.invoke(FunctionName="final-lex-bot-v1-dev-text_audio_translater", Payload = json.dumps(event))
        payload = json.load(invoke_response['Payload'])
        return payload
    
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