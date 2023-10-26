import boto3
from utils.check_has_text       import check_has_text
from utils.decode_response_data import decode_response_data

rekognition = boto3.client("rekognition")

def extract_text_from_image(BUCKET_NAME, IMAGE_NAME):
  """
  Extracts text from an image stored in an S3 bucket using Amazon Rekognition.

  Args:
  - BUCKET_NAME (str): The name of the S3 bucket where the image is stored.
  - IMAGE_NAME (str): The name of the image file in the S3 bucket.

  Returns:
  - str: The text extracted from the image, or a message indicating that no text was found in the image.

  Raises:
  - Exception: If there is an error while processing the image.

  """
  try:
    bucket = BUCKET_NAME
    key    = IMAGE_NAME

    response  = rekognition.detect_text(
        Image = {"S3Object": {"Bucket": bucket, "Name": key}}
    )

    has_text = check_has_text(response["TextDetections"])

    if not has_text:
      no_text_phrase          = "Não foi encontrado texto na imagem!"
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
    print(f"Error rekognition service: {e}")