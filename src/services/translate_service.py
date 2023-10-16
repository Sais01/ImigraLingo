import boto3

def text_translate(text, source_language, target_language):
    # Configure o cliente do Amazon Translate
    translate_client = boto3.client('translate', region_name='us-east-1')

    # Realize a tradução
    result = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )

    # Extraia o texto traduzido do resultado
    translated_text = result['TranslatedText']

    return translated_text