import boto3

def text_translate(text, source_language, target_language):
  try:
    # Configure the Amazon Translate client
    translate_client = boto3.client('translate', region_name='us-east-1')

    # Perform the translation
    result = translate_client.translate_text(
      Text=text,
      SourceLanguageCode=source_language,
      TargetLanguageCode=target_language
    )

    # Extract the translated text from the result
    translated_text = result['TranslatedText']

    return translated_text
  
  except Exception as e:
    # Handle exceptions here
    print(e)
    return None

# if __name__ == "__main__":
#   print(text_translate("batata", "pt", "fr"))