import boto3

s3_client    = boto3.client("s3")
polly_client = boto3.client("polly")

def text_converter(text, language):
  """
  Converts text to speech using Amazon Polly service.

  Args:
  text (str): The text to be converted to speech.
  language (str): The language of the text. Can be 'fr' for French or 'pt' for Portuguese.

  Returns:
  bytes: The audio stream of the synthesized speech in mp3 format.

  """
  try:
    response = polly_client.synthesize_speech(
      OutputFormat = 'mp3',
      Text         = text,
      VoiceId      = 'Lea' if language == 'fr' else 'Camila',
      LanguageCode = 'fr-FR' if language == 'fr' else 'pt-BR'
    )

    return response["AudioStream"].read()
  
  except Exception as e:
    print(f"Error text converter: {e}")

    return None


def text_converted_s3_upload(audio, bucket_name, audio_name):
  """
  Uploads an audio file to an S3 bucket and returns the URL of the uploaded file.

  Args:
    audio (bytes): The audio file to be uploaded.
    bucket_name (str): The name of the S3 bucket to upload the file to.
    audio_name (str): The name of the audio file to be uploaded.

  Returns:
    str: The URL of the uploaded audio file.
  """

  s3_client.put_object(
    Body        = audio,
    Bucket      = bucket_name,
    Key         = audio_name,
    ContentType = 'audio/mpeg'
  )

  url = f"https://{bucket_name}.s3.amazonaws.com/{audio_name}"
  
  return url