import os

class Settings:
    TWILIO_WHATS_FROM = os.getenv("TWILIO_WHATS_FROM")
    TWILIO_WHATS_TO = os.getenv("TWILIO_WHATS_TO")
    TWILIO_ID = os.getenv("TWILIO_ID")
    TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    START_CONVERSATION_MESSAGE = os.getenv("START_CONVERSATION_MESSAGE")

settings = Settings()