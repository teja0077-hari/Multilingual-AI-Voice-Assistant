from gnani.tts import GnaniTTSClient, AudioConfig

from config import GNANI_API_KEY_ID


def generate_speech(text, language):

    if not GNANI_API_KEY_ID:
        raise ValueError("Gnani API key is missing.")

    if not text or not text.strip():
        raise ValueError("No text provided for speech generation.")

    language_codes = {
        "Telugu": "te-IN",
        "Hindi": "hi-IN",
        "English": "en-IN"
    }

    if language not in language_codes:
        raise ValueError("Unsupported language.")

    client = GnaniTTSClient(
        api_key=GNANI_API_KEY_ID
    )

    audio = client.synthesize(
        text,
        voice="Kaveri",
        model="timbre-v2.5",
        language=language_codes[language],
        speed=1.0,
        audio_config=AudioConfig(
            container="wav",
            sample_rate=22050,
            encoding="linear_pcm"
        )
    )

    return audio