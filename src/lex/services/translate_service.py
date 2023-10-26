import boto3

def text_translate(text: str, source_language: str, target_language: str) -> str:
  """
  Translates the given text from the source language to the target language using AWS Translate service.

  Args:
    text (str): The text to be translated.
    source_language (str): The language code of the source language.
    target_language (str): The language code of the target language.

  Returns:
    str: The translated text.

  Raises:
    Exception: If there is an error while translating the text.
  """
  try:
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
    print(f"Error text translater: {e}")
    return None