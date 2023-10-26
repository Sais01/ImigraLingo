import os

class Settings:
  IMAGE_NAME               = os.getenv("IMAGE_NAME")
  AUDIO_NAME               = os.getenv("AUDIO_NAME")
  BUCKET_NAME              = os.getenv("BUCKET_NAME")
  NUMBER_OF_PLACES         = os.getenv("NUMBER_OF_PLACES")
  VIA_CEP_BASE_URL         = os.getenv("VIA_CEP_BASE_URL")
  AROUND_SEARCH_PLACES     = os.getenv("AROUND_SEARCH_PLACES")
  OVERPASS_API_BASE_URL    = os.getenv("OVERPASS_API_BASE_URL")
  OPENSTREETMAP_BASE_URL   = os.getenv("OPENSTREETMAP_BASE_URL")
  API_KEY_OPENCAGE_GEOCODE = os.getenv("API_KEY_OPENCAGE_GEOCODE")

settings = Settings()