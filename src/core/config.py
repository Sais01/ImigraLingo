import os

class Settings:
    API_KEY_OPENCAGE_GEOCODE = os.getenv("API_KEY_OPENCAGE_GEOCODE")
    
settings = Settings()