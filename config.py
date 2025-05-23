from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    DB_URI = os.getenv("DB_URI")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-pro")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
    MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "3"))
    VERBOSE = os.getenv("VERBOSE", "true").lower() == "true"


settings = Settings
