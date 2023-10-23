from datetime import datetime
# from core.config import settings
# import json
import boto3

s3_client    = boto3.client("s3", region_name="us-east-1")
polly_client = boto3.client("polly", region_name="us-east-1")
voicePolly   = "Camila"

def text_converter(text):

  response = polly_client.synthesize_speech(
    VoiceId      = voicePolly,
    Text         = text,
    OutputFormat = "mp3",
    LanguageCode = "pt-BR"
  )

  return response["AudioStream"].read()


def text_converted_s3_upload(receivedText, AUDIO_NAME, BUCKET_NAME):

    s3_client.put_object(
        Body   = text_converter(receivedText),
        Bucket = BUCKET_NAME,
        Key    = AUDIO_NAME,  # Chave com o nome do objeto
        ContentType='audio/mpeg'
    )

    url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{AUDIO_NAME}"

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