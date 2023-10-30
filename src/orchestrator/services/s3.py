import boto3
import uuid
import requests


def upload_s3(bucket_name, media_url, media_format):
    try:
      s3 = boto3.client('s3')                
      # Get the image data from the URL
      response = requests.get(media_url)

      if response.status_code == 200:
        # Specify the S3 object key (the filename in the S3 bucket)
        object_name = f"{str(uuid.uuid4())}.{media_format}"

        # Upload the image to S3
        s3.put_object(Bucket=bucket_name, Key=object_name, Body=response.content)
        print(f"Media uploaded to S3 bucket '{bucket_name}' with key '{object_name}'")
        return object_name

    except Exception as e:
      print(f"An error occurred download Image: {e}")

