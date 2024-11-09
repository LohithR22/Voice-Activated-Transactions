# transcriber.py
import speech_recognition as sr

def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Recording...")
        audio = recognizer.listen(source)
        print("Recording stopped.")
    return audio

def transcribe_audio(audio):
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Service unavailable"
