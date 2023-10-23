from core.config import settings
from services.rekognition_service import extract_text_from_image
from utils.response_formatters import prepare_response_text
from services.translate_service import text_translate

def handle_image_to_text(event, context):
    try:
        BUCKET_NAME = settings.BUCKET_NAME
        
        slots = event['interpretations'][0]['intent']['slots']
        image_name = slots['imgFromUser']['value']['originalValue']
        text_or_audio_conditional = slots['textOrAudioConditional']['value']['originalValue']

        response_text_from_image = extract_text_from_image(BUCKET_NAME, image_name)

        text_from_image = response_text_from_image["body"]["phrase"]

        if text_or_audio_conditional == "text_fr":
            text_from_image = text_translate(text_from_image, "pt", "fr")
            return prepare_response_text(event, text_from_image)
        
        elif text_or_audio_conditional == "audio_pt":
            return prepare_response_text(event, text_from_image)
        
        elif text_or_audio_conditional == "audio_fr":
            return prepare_response_text(event, text_from_image)
        else:
            return prepare_response_text(event, text_from_image)

        print("1######################")
        print(response_text_from_image["body"])
        print("1@@@@@@@@@@@@@@@@@@@@@@")

        print("2######################")
        print(text_from_image)
        print("2@@@@@@@@@@@@@@@@@@@@@@")

        

    except Exception as e:
        print(f"Error in image_text_extraction_controller: {e}")
        return prepare_response_text(
            event, f"Erreur lors du traitement de la demande d'achat: {str(e)}"
        )

