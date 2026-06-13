from faster_whisper import WhisperModel

print("Loading...")

try:

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

    print("SUCCESS")

except Exception as e:

    print(type(e))
    print(e)