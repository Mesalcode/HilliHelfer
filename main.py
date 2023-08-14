#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import sounddevice

import speech_recognition as sr

while True:

    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Warte auf Frage..")
        audio = r.listen(source)

    try:
        recognized_sentence = r.recognize_google(audio, language="de-DE")

        print("Erkannter Satz: " + recognize_google)

        if "assistent" in recognized_sentence.lower():
            print("Ich fühle mich angesprochen.")
    except sr.UnknownValueError:
        print("Dies konnte nicht verstanden werden.")
    except sr.RequestError as e:
        print("Dies konnte nicht verarbeitet werden.")