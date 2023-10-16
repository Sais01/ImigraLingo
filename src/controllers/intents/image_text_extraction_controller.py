# def handle_image_text_extraction():
#   pass

import json
import boto3

rekognition = boto3.client('rekognition')

def image_to_text_handler(event, context):
    # The S3 bucket and object key where the image is stored
    # bucket = event['Records'][0]['s3']['bucket']['name']
    # key = event['Records'][0]['s3']['object']['key']

    try: 
      bucket = "teste-bucket-mathsp-segundo"
      key = "placa-seguranca.jpg"

      # Detect text in the image
      response = rekognition.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': key}})

      detected_text = []
      for item in response['TextDetections']:
          detected_text.append(item['DetectedText'])

      print(detected_text)

      return {
          'statusCode': 200,
          'body': json.dumps(detected_text)
      }
    
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print("Olá mundo")