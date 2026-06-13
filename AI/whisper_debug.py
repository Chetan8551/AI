import whisper

print("Starting...")

try:
    model = whisper.load_model("tiny")
    print("SUCCESS")
except Exception as e:
    print("ERROR:")
    print(type(e))
    print(e)