from core.config import settings
from services.rekognition_service import extract_text_from_image
from utils.response_formatters import prepare_response_text
from services.translate_service import text_translate
from services.polly_service import text_converter, text_converted_s3_upload

def handle_image_to_text(event, context):
    try:
        BUCKET_NAME = settings.BUCKET_NAME
        
        slots = event['interpretations'][0]['intent']['slots']
        image_name = slots['imgFromUser']['value']['originalValue']
        text_or_audio_conditional = slots['textOrAudioConditional']['value']['originalValue']

        response_text_from_image = extract_text_from_image(BUCKET_NAME, image_name)

        text_from_image = response_text_from_image["body"]["phrase"]
        response = text_from_image

        if text_or_audio_conditional == "text_fr":
            translate_response = text_translate(text_from_image, "pt", "fr")
            return prepare_response_text(event, translate_response)
        
        elif text_or_audio_conditional == "audio_pt":
            audio_response = text_converter(text_from_image, "pt")
            audio_s3_response = text_converted_s3_upload(audio_response, BUCKET_NAME, "teste")
            return prepare_response_text(event, audio_s3_response)
        
        elif text_or_audio_conditional == "audio_fr":
            translate_response = text_translate(text_from_image, "pt", "fr")
            audio_response = text_converter(translate_response, "fr")
            audio_s3_response = text_converted_s3_upload(audio_response, BUCKET_NAME, "teste")
            return prepare_response_text(event, audio_s3_response)
        else:
            return prepare_response_text(event, response)

    except Exception as e:
        print(f"Error in image_text_extraction_controller: {e}")
        return prepare_response_text(
            event, f"Erreur lors du traitement de la demande d'achat: {str(e)}"
        )

