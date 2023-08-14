import speech_recognition as sr

with sr.Microphone() as source:
    # read the audio data from the default microphone
    audio_data = sr.record(source, duration=5)
    print("Recognizing...")
    # convert speech to text
    text = sr.recognize_google(audio_data, language="de-DE")
    print(text)