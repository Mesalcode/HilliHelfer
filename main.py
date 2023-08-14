#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

while True:

    # obtain audio from the microphone
    r = sr.Recognizer()
    with noalsaerr() as n, sr.Microphone() as source:
        print("Warte auf Frage..")
        audio = r.listen(source)

    try:
        print("Erkannter Satz: " + r.recognize_google(audio, language="de-DE"))
    except sr.UnknownValueError:
        print("Dies konnte nicht verstanden werden.")
    except sr.RequestError as e:
        print("Dies konnte nicht verarbeitet werden.")