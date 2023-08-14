#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

from ctypes import *
from contextlib import contextmanager
import pyaudio

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

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