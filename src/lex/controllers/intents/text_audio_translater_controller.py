from core.config                 import settings
from services.polly_service      import text_converter, text_converted_s3_upload
from services.translate_service  import text_translate
from services.transcribe_service import audio_to_text
from utils.response_formatters   import prepare_response_text

def handle_text_audio_translater(event, context):
  try:
    bucket_name = settings.BUCKET_NAME

    slots                          = event['interpretations'][0]['intent']['slots']

    text_or_audio_user_input       = slots["textOrAudioUserInput"]["value"]["originalValue"]
    user_language_conditional      = slots["languageConditional"]["value"]["originalValue"]
    user_text_or_audio_receiver    = slots["textOrAudioReceiver"]["value"]["originalValue"]
    user_text_or_audio_conditional = slots["textOrAudioConditional"]["value"]["originalValue"]

    if (user_language_conditional == "ptToFr"):
      language = "pt-BR"
      if (text_or_audio_user_input == "audio"):
        text_to_translate = audio_to_text(user_text_or_audio_receiver, language, bucket_name)
      else:
        text_to_translate = user_text_or_audio_receiver
    else:
      language = "fr-FR"
      if (text_or_audio_user_input == "audio"):
        text_to_translate = audio_to_text(user_text_or_audio_receiver, language, bucket_name)
      else:
        text_to_translate = user_text_or_audio_receiver


    if (user_language_conditional == "ptToFr"):
      text_or_audio_translated = text_translate(text_to_translate, "pt", "fr")

      if (user_text_or_audio_conditional == "text"):
        return prepare_response_text(event, text_or_audio_translated)
      
      if (user_text_or_audio_conditional == "audio"):
        audio_response = text_converter(text_or_audio_translated, "fr")
        audio_s3_response = text_converted_s3_upload(audio_response, bucket_name, "testeAudioTranslate")
        return prepare_response_text(event, audio_s3_response)

    elif (user_language_conditional == "frToPt"):
      text_or_audio_translated = text_translate(text_to_translate, "fr", "pt")

      if (user_text_or_audio_conditional == "text"):
        return prepare_response_text(event, text_or_audio_translated)
        
      elif (user_text_or_audio_conditional == "audio"):
        audio_response = text_converter(text_or_audio_translated, "pt")
        audio_s3_response = text_converted_s3_upload(audio_response, bucket_name, "testeAudioTranslate")
        return prepare_response_text(event, audio_s3_response)
        
  except Exception as e:
    print(f"Error in image_text_extraction_controller: {e}")
    return prepare_response_text(
      event, f"Erreur lors du traitement de la demande d'achat: {str(e)}"
    )