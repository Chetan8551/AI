from modules.tts import speak
from modules.speech import (
    record_audio,
    transcribe_audio
)

print("Starting Voice Test")

speak("Voice system initialized")

audio_file = record_audio()

text = transcribe_audio(audio_file)

print("\nYou said:")
print(text)

if text:
    speak(f"You said {text}")
else:
    speak("Sorry boss, I could not hear anything.")