import speech_recognition as sr

RECOGNIZER = sr.Recognizer()

RECOGNIZER.energy_threshold = 300
RECOGNIZER.pause_threshold = 0.8
RECOGNIZER.dynamic_energy_threshold = True


def listen_once():
    with sr.Microphone() as source:
        print("\nListening... Speak now!")
        RECOGNIZER.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = RECOGNIZER.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

    try:
        text = RECOGNIZER.recognize_google(audio, language="en-IN")
        text = text.strip()

        print("\nDetected:")
        print(text)

        return text

    except sr.UnknownValueError:
        try:
            text = RECOGNIZER.recognize_google(audio, language="hi-IN")
            text = text.strip()

            print("\nDetected:")
            print(text)

            return text

        except sr.UnknownValueError:
            print("Sorry, I could not understand.")
            return ""

        except sr.RequestError as e:
            print(f"Google Speech Recognition error: {e}")
            return ""

    except sr.RequestError as e:
        print(f"Google Speech Recognition error: {e}")
        return ""