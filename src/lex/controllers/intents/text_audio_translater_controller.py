from core.config                 import settings
from services.polly_service      import text_converter, text_converted_s3_upload
from services.translate_service  import text_translate
from services.transcribe_service import audio_to_text
from utils.response_formatters   import prepare_response_text
import uuid

def handle_text_audio_translater(event, context):
  """
  Handles the text/audio translation request by extracting the necessary information from the event object,
  translating the text/audio to the desired language, and returning the translated text/audio as a response.

  Args:
    event (dict): The event object containing the user input and other relevant information.
    context (dict): The context object containing the runtime information.

  Returns:
    dict: The response object containing the translated text/audio.
  """
  try:
    bucket_name = settings.BUCKET_NAME

    slots                          = event['interpretations'][0]['intent']['slots']

    text_or_audio_user_input       = slots["textOrAudioUserInput"]["value"]["originalValue"]
    user_language_conditional      = slots["languageConditional"]["value"]["originalValue"]
    user_text_or_audio_receiver    = slots["textOrAudioReceiver"]["value"]["originalValue"]
    user_text_or_audio_conditional = slots["textOrAudioConditional"]["value"]["originalValue"]

 
    if user_language_conditional == "ptToFr":
      from_lang_translate_and_polly = "pt"
      to_lang_translate_and_polly   = "fr"
      language_audio_transcribe = "pt-BR"
    else:
      from_lang_translate_and_polly = "fr"
      to_lang_translate_and_polly = "pt"
      language_audio_transcribe = "fr-FR"

    
    if (text_or_audio_user_input == "audio"):
      text_to_translate = audio_to_text(user_text_or_audio_receiver, language_audio_transcribe, bucket_name)
    else:
      text_to_translate = user_text_or_audio_receiver


    text_or_audio_translated = text_translate(text_to_translate, from_lang_translate_and_polly, to_lang_translate_and_polly)

    if (user_text_or_audio_conditional == "text"):
      return prepare_response_text(event, text_or_audio_translated)
    else:
      audio_response = text_converter(text_or_audio_translated, to_lang_translate_and_polly)
      audio_s3_response = text_converted_s3_upload(audio_response, bucket_name, str(uuid.uuid4()))
      return prepare_response_text(event, audio_s3_response)
        
  except Exception as e:
    print(f"Error in image_text_extraction_controller: {e}")
    return prepare_response_text(
      event, f"Erreur lors du traitement de la demande d'achat: {str(e)}"
    )