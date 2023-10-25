import boto3

def audio_to_text(audio, language_code):
  try:
    # Configure the Amazon Transcribe client
    transcribe_client = boto3.client('transcribe', region_name='us-east-1')

    # Perform audio-to-text conversion
    response = transcribe_client.start_transcription_job(
      TranscriptionJobName='audio-to-text-job',
      LanguageCode=language_code,
      MediaFormat='audio/wav',  # Correct format of audio
      Media={
        'MediaFileUri': audio  # URL of audio file in AWS S3 or local path
      },
      OutputBucketName='your-s3-bucket'  # Name of S3 bucket where the result will be stored
    )

    # Wait until the transcription job is complete
    job_name = response['TranscriptionJob']['TranscriptionJobName']
    transcribe_client.get_waiter('transcription_job_completed').wait(TranscriptionJobName=job_name)

    # Retrieve the transcription result
    result_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']

    # Download the transcription file
    s3 = boto3.client('s3')
    result = s3.get_object(Bucket='your-s3-bucket', Key=result_uri[len('s3://'):])
    text = result['Body'].read().decode('utf-8')

    return text

  except Exception as e:
    # Capture any exception that occurs and print the error message
    print(f"An error occurred: {str(e)}")
    return None  # You can choose how to handle the error, in this case, we return None
