import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name = os.getenv("APP_NAME", "EduGenie")
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    gemini_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


settings = Settings()

APP_NAME = settings.app_name
GEMINI_MODEL = settings.gemini_model
GEMINI_API_KEY = settings.gemini_api_key