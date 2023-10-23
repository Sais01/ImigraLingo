from datetime import datetime
# from core.config import settings
# import json
import boto3

s3_client    = boto3.client("s3")
polly_client = boto3.client("polly")

def text_converter(text, language):
  try:
    response = polly_client.synthesize_speech(
      OutputFormat='mp3',
      Text=text,
      VoiceId='Lea' if language == 'fr' else 'Camila',
      LanguageCode='fr-FR' if language == 'fr' else 'pt-BR'
    )

    return response["AudioStream"].read()
  
  except Exception as e:
    print(f"Error text converter: {e}")
    return None


def text_converted_s3_upload(audio, bucket_name, audio_name):

    s3_client.put_object(
        Body   = audio,
        Bucket = bucket_name,
        Key    = audio_name,  # Chave com o nome do objeto
        ContentType='audio/mpeg'
    )

    url = f"https://{bucket_name}.s3.amazonaws.com/{audio_name}"

    return url


# def tts(event, context):
#     try:
#         # Recebe o body da requisição
#         body = json.loads(event["body"])

#         # Recebe a frase e a data de criação
#         received_phrase = body["phrase"]
#         created_time = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

#         # Chama a função para o upload do audio no S3
#         audio_s3 = text_converted_s3_upload(received_phrase, created_time)

#         response_body = {
#             "received_phrase": received_phrase,
#             "url_to_audio": audio_s3,
#             "created_audio": created_time,
#         }

#         response = {"statusCode": 200,
#                     "body": json.dumps(response_body),
#                     "headers": {
#                         "Access-Control-Allow-Origin": "*",
#                         "Content-Type": "application/json"
#                     }}

#         return response
#     except Exception as e:
#         response = {"statusCode": 500,
#                     "body": json.dumps(f"Error: {e}"),
#                     "headers": {
#                         "Access-Control-Allow-Origin": "*",
#                         "Content-Type": "application/json"
#                     }}
#         return response
    
# if __name__ == "__main__":
#   texto = "Olá, tudo bem?"
#   print(texto)
#   print(text_converted_s3_upload(texto, "teste.mp3", "finallexbotv1"))