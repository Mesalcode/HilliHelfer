#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

#import thorsten

#thorsten.say("Guten Morgen! Ich bin Thomas Hillebrand. Brauchst du mit etwas Hilfe? Sag einfach Bescheid!")

import voice_recognition

exit(0)

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

        print("Erkannter Satz: " + recognized_sentence)

        if "assisten" in recognized_sentence.lower():
            print("Ich fühle mich angesprochen.")
    except sr.UnknownValueError as u:
        print(u)
        print("Dies konnte nicht verstanden werden.")
    except sr.RequestError as e:
        print(e)
        print("Dies konnte nicht verarbeitet werden.")