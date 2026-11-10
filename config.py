
import os
from dotenv import load_dotenv

load_dotenv()

# Gnani API configuration
GNANI_API_KEY_ID = os.getenv("GNANI_API_KEY_ID")
GNANI_STT_URL = "https://api.vachana.ai/stt/v3"

# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Supported languages
LANGUAGE_CODES = {
    "Telugu": "te-IN",
    "Hindi": "hi-IN",
    "English": "en-IN"
}


def validate_config():
    if not GNANI_API_KEY_ID:
        raise ValueError(
            "Gnani API key is missing. Check your .env file."
        )

    if not GROQ_API_KEY:
        raise ValueError(
            "Groq API key is missing. Check your .env file."
        )
