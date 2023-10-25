import boto3
from core.config import settings
from utils.decode_response_data import decode_response_data
from utils.check_has_text import check_has_text

rekognition = boto3.client("rekognition")

# BUCKET_NAME = settings.BUCKET_NAME
# IMAGE_NAME = settings.IMAGE_NAME


def extract_text_from_image(BUCKET_NAME, IMAGE_NAME):
    try:
        bucket = BUCKET_NAME
        key = IMAGE_NAME

        # Detect text in the image
        response = rekognition.detect_text(
            Image={"S3Object": {"Bucket": bucket, "Name": key}}
        )

        has_text = check_has_text(response["TextDetections"])
        if not has_text:
            no_text_phrase = "Não foi encontrado texto na imagem!"
            no_text_phrase_response = decode_response_data(no_text_phrase)

            return no_text_phrase_response

        else:
            text_phrase = ""
            for item in response["TextDetections"]:
                if item["Type"] == "WORD" and item["Confidence"] >= 50:
                    text_phrase += str(item["DetectedText"]) + " "

            text_phrase = text_phrase[:-1]

            text_phrase_response = decode_response_data(text_phrase)

            return text_phrase_response

    except Exception as e:
        print(e)
