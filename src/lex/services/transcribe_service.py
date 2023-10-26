import boto3
import json
import uuid

def audio_to_text(audio_name, language, bucket_name):
  try:
    transcribe_client = boto3.client('transcribe')
    job_name = str(uuid.uuid4())
    audio_s3_path = f's3://{bucket_name}/{audio_name}'

    # Define transcription job settings
    settings = {
        'TranscriptionJobName': job_name,
        'LanguageCode': language,
        'MediaFormat': 'mp3', 
        'Media': {'MediaFileUri': audio_s3_path},
        'OutputBucketName': bucket_name
    }

    # Start the transcription job
    transcribe_client.start_transcription_job(**settings)

    # Wait until the transcription job is completed
    while True:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        status = response['TranscriptionJob']['TranscriptionJobStatus']
        if status in ['COMPLETED', 'FAILED']:
            break

    # Check if transcription was completed successfully
    if status == 'COMPLETED':
        result_transcription = boto3.client('s3').get_object(Bucket=bucket_name, Key=f'{job_name}.json')

        transcribed_text = result_transcription['Body'].read()
        data = json.loads(transcribed_text)

        transcript = data['results']['transcripts'][0]['transcript']
        print(transcript)

        return transcript
    else:
        return None

  except Exception as e:
    print(f"An error occurred: {str(e)}")
    return None

