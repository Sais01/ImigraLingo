import os

class Settings:
    API_KEY_OPENCAGE_GEOCODE = os.getenv("API_KEY_OPENCAGE_GEOCODE")
    AROUND_SEARCH_PLACES = os.getenv("AROUND_SEARCH_PLACES")
    NUMBER_OF_PLACES = os.getenv("NUMBER_OF_PLACES")
    VIA_CEP_BASE_URL = os.getenv("VIA_CEP_BASE_URL")
    OVERPASS_API_BASE_URL = os.getenv("OVERPASS_API_BASE_URL")
    OPENSTREETMAP_BASE_URL = os.getenv("OPENSTREETMAP_BASE_URL")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    IMAGE_NAME = os.getenv("IMAGE_NAME")
    AUDIO_NAME = os.getenv("AUDIO_NAME")

settings = Settings()