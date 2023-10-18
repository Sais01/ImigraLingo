import boto3
from core.config import settings
from utils.decode_response_data import decode_response_data
from utils.check_has_text import check_has_text

rekognition = boto3.client("rekognition")

BUCKET_NAME = settings.BUCKET_NAME
IMAGE_NAME = settings.IMAGE_NAME

def image_to_text_handler(event, context):
    try:
        bucket = BUCKET_NAME
        key = IMAGE_NAME

        # Detect text in the image
        response = rekognition.detect_text(
            Image={"S3Object": {"Bucket": bucket, "Name": key}}
        )

        has_text = check_has_text(response["TextDetections"])
        if not has_text:
            no_text_message = "Não foi encontrado texto na imagem!"
            
            return {"statusCode": 200, "body": no_text_message}
        
        detected_text = []
        for item in response["TextDetections"]:
            if item["Type"] == "WORD" and item["Confidence"] >= 50:
                detected_text.append(item["DetectedText"])

        decoded_data = decode_response_data(detected_text)

        return {"statusCode": 200, "body": decoded_data}

    except Exception as e:
        print(e)


# if __name__ == '__main__':
