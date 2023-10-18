import json
import boto3
from core.config import settings

rekognition = boto3.client("rekognition")

BUCKET_NAME = settings.BUCKET_NAME
IMAGE_NAME = settings.IMAGE_NAME


def format_response_data(response_data):
    json_data = json.dumps(response_data)
    decoded_data = json_data.encode("utf-8").decode("unicode-escape")
    decoded_data = decoded_data.replace('"', "'")

    return decoded_data


def image_to_text_handler(event, context):
    try:
        bucket = BUCKET_NAME
        key = IMAGE_NAME

        # Detect text in the image
        response = rekognition.detect_text(
            Image={"S3Object": {"Bucket": bucket, "Name": key}}
        )

        detected_text = []
        for item in response["TextDetections"]:
            if item["Type"] == "WORD" and item["Confidence"] >= 50:
                detected_text.append(item["DetectedText"])

        decoded_data = format_response_data(detected_text)

        return {"statusCode": 200, "body": decoded_data}

    except Exception as e:
        print(e)


# if __name__ == '__main__':
