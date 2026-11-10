
import io
import wave
import json
import requests

from config import (
    GNANI_API_KEY_ID,
    GNANI_STT_URL,
    LANGUAGE_CODES,
    validate_config
)


def transcribe_audio(audio_bytes, language):

    # ==========================================
    # CONFIGURATION VALIDATION
    # ==========================================

    validate_config()

    if not audio_bytes:
        raise ValueError("No audio recording provided.")

    if language not in LANGUAGE_CODES:
        raise ValueError(f"Unsupported language: {language}")

    # ==========================================
    # INSPECT RECORDED WAV FILE
    # ==========================================

    try:
        with wave.open(io.BytesIO(audio_bytes), "rb") as wav:

            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            sample_rate = wav.getframerate()
            frames = wav.getnframes()

            duration = (
                frames / sample_rate
                if sample_rate else 0
            )

            audio_info = (
                f"File size: {len(audio_bytes)} bytes, "
                f"Duration: {duration:.2f} seconds, "
                f"Sample rate: {sample_rate} Hz, "
                f"Channels: {channels}, "
                f"Sample width: {sample_width * 8} bits"
            )

    except Exception as error:
        raise RuntimeError(
            f"Could not read the recording as WAV: {error}. "
            f"File size: {len(audio_bytes)} bytes."
        )

    if duration <= 0:
        raise RuntimeError(
            f"Recording has no audio frames. {audio_info}"
        )

    if duration > 60:
        raise RuntimeError(
            "Recording is longer than Gnani's documented "
            f"60-second REST limit. {audio_info}"
        )

    # ==========================================
    # LANGUAGE CONFIGURATION
    # ==========================================

    language_code = LANGUAGE_CODES[language]

    headers = {
        "X-API-Key-ID": GNANI_API_KEY_ID
    }

    payload = {
        "language_code": language_code,
        "preferred_language": language_code,
        "format": "transcribe",
        "itn_native_numerals": "true"
    }

    files = {
        "audio_file": (
            "recording.wav",
            audio_bytes,
            "audio/wav"
        )
    }

    # ==========================================
    # GNANI SPEECH-TO-TEXT API REQUEST
    # ==========================================

    try:

        response = requests.post(
            GNANI_STT_URL,
            headers=headers,
            data=payload,
            files=files,
            timeout=120
        )

        response.raise_for_status()

        # ==========================================
        # READ API RESPONSE
        # ==========================================

        try:
            result = response.json()

        except ValueError:
            raise RuntimeError(
                "Gnani returned an invalid JSON response.\n"
                f"HTTP status: {response.status_code}\n"
                f"Response: {response.text[:2000]}"
            )

        if not isinstance(result, dict):
            raise RuntimeError(
                "Gnani returned an unexpected response format.\n"
                f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}"
            )

        # ==========================================
        # CHECK API SUCCESS
        # ==========================================

        if not result.get("success"):
            raise RuntimeError(
                "Gnani transcription failed.\n"
                "Complete API response:\n"
                f"{json.dumps(result, indent=2, ensure_ascii=False)}"
            )

        # ==========================================
        # EXTRACT TRANSCRIPT
        # ==========================================

        transcript = result.get("transcript", "")

        if isinstance(transcript, str):
            transcript = transcript.strip()
        else:
            transcript = ""

        # ==========================================
        # HANDLE EMPTY TRANSCRIPTION
        # ==========================================

        if not transcript:

            raise RuntimeError(
                "Gnani returned success but no transcript.\n\n"

                f"Audio details:\n{audio_info}\n\n"

                f"Language sent: {language_code}\n"
                f"HTTP status: {response.status_code}\n\n"

                f"Response keys: {list(result.keys())}\n\n"

                "Complete API response:\n"
                f"{json.dumps(result, indent=2, ensure_ascii=False)}"
            )

        # ==========================================
        # RETURN TRANSCRIBED TEXT
        # ==========================================

        return transcript

    # ==========================================
    # ERROR HANDLING
    # ==========================================

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Gnani API request timed out. "
            "Please try again in a moment."
        )

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"Gnani API error: {error}\n"
            f"HTTP status: {response.status_code}\n"
            f"Details: {response.text[:2000]}"
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Connection error: {error}"
        )
