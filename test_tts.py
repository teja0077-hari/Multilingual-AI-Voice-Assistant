
from pathlib import Path
from tts import generate_speech

try:
    print("Testing Gnani Timbre...")

    text = "Hello! Welcome to my multilingual AI voice assistant."

    audio = generate_speech(text, "English")

    folder = Path("outputs/generated_audio")
    folder.mkdir(parents=True, exist_ok=True)

    output = folder / "test_voice.wav"
    output.write_bytes(audio)

    print("SUCCESS! Audio generated.")
    print("Saved at:", output)

except Exception as error:
    print("ERROR:", error)
