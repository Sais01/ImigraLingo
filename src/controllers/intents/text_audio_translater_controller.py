from core.config                 import settings
from services.polly_service      import text_converted_s3_upload
from services.translate_service  import text_translate
from services.transcribe_service import audio_to_text
from utils.response_formatters   import prepare_response_text

def handle_text_audio_translater(event, context):
    BUCKET_NAME = settings.BUCKET_NAME
    AUDIO_NAME  = settings.AUDIO_NAME

    slots                      = event['interpretations'][0]['intent']['slots']
    userLanguageConditional    = slots["languageConditional"]["value"]["originalValue"]
    userTextOrAudioReceiver    = slots["textOrAudioReceiver"]["value"]["originalValue"]
    userTextOrAudioConditional = slots["textOrAudioConditional"]["value"]["originalValue"]

    if (userLanguageConditional == "ptToFr"):
      textOrAudioTranslated = text_translate(str(userTextOrAudioReceiver), "pt", "fr")

      try:
        if (userTextOrAudioConditional == "text"):
          return prepare_response_text(event, textOrAudioTranslated)
        
      except Exception as e:
        print(f"Error in handle_text_audio_translater: {e}")
        return prepare_response_text(
          event, f"erro text: {str(e)}"
        )
      
      try:
        if (userTextOrAudioConditional == "audio"):
          textOrAudioTranslated_S3Upload = text_converted_s3_upload(textOrAudioTranslated, AUDIO_NAME, BUCKET_NAME)

          return prepare_response_text(event, textOrAudioTranslated_S3Upload)
        
      except Exception as e:
        print(f"Error in handle_text_audio_translater: {e}")
        return prepare_response_text(
          event, f"erro audio: {str(e)}"
        )
        
    try:
      if (userLanguageConditional == "frToPt"):
        textOrAudioTranslated = text_translate(userTextOrAudioReceiver, "fr", "pt")

        if (userTextOrAudioConditional == "text"):
          return prepare_response_text(event, textOrAudioTranslated)
        
        if (userTextOrAudioConditional == "audio"):
          textOrAudioTranslated_S3Upload = text_converted_s3_upload(textOrAudioTranslated, AUDIO_NAME, BUCKET_NAME)
          return prepare_response_text(event, textOrAudioTranslated_S3Upload)
        
    except Exception as e:
      print(f"Error in handle_text_audio_translater: {e}")
      return prepare_response_text(
        event, f"erro frToPt: {str(e)}"
      )