# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")

settings = Settings()
