from core.config                 import settings
from services.polly_service      import text_converter, text_converted_s3_upload
from services.translate_service  import text_translate
from services.transcribe_service import audio_to_text
from utils.response_formatters   import prepare_response_text

def handle_text_audio_translater(event, context):
  try:
    BUCKET_NAME = settings.BUCKET_NAME

    slots                      = event['interpretations'][0]['intent']['slots']
    userLanguageConditional    = slots["languageConditional"]["value"]["originalValue"]
    userTextOrAudioReceiver    = slots["textOrAudioReceiver"]["value"]["originalValue"]
    userTextOrAudioConditional = slots["textOrAudioConditional"]["value"]["originalValue"]

    if (userLanguageConditional == "ptToFr"):
      textOrAudioTranslated = text_translate(userTextOrAudioReceiver, "pt", "fr")

      if (userTextOrAudioConditional == "text"):
        return prepare_response_text(event, textOrAudioTranslated)
      
      if (userTextOrAudioConditional == "audio"):
        audio_response = text_converter(textOrAudioTranslated, "fr")
        audio_s3_response = text_converted_s3_upload(audio_response, BUCKET_NAME, "testeAudioTranslate")
        return prepare_response_text(event, audio_s3_response)

    elif (userLanguageConditional == "frToPt"):
      textOrAudioTranslated = text_translate(userTextOrAudioReceiver, "fr", "pt")

      if (userTextOrAudioConditional == "text"):
        return prepare_response_text(event, textOrAudioTranslated)
        
      elif (userTextOrAudioConditional == "audio"):
        audio_response = text_converter(textOrAudioTranslated, "pt")
        audio_s3_response = text_converted_s3_upload(audio_response, BUCKET_NAME, "testeAudioTranslate")
        return prepare_response_text(event, audio_s3_response)
        
  except Exception as e:
    print(f"Error in image_text_extraction_controller: {e}")
    return prepare_response_text(
      event, f"Erreur lors du traitement de la demande d'achat: {str(e)}"
    )