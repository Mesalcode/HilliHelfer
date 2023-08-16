from TTS.api import TTS
import sounddevice
import regex as re
import time
from playsound import playsound
import soundfile as sf
import requests
import time

tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False, gpu=False)

def say(text):
    start = time.time()

    special_char_map = {ord('ä'):'ae', ord('Ä'):'Ae', ord('ü'):'ue', ord('Ü'):'Ue', ord('ö'):'oe', ord('Ö'):'Oe', ord('ß'):'ss'}
    text = text.translate(special_char_map)

    #abbreviations_map = {'bzw.': 'beziehungsweise', 'usw.': 'und so weiter', 'bzgl.':'bezüglich', 'ggf': 'gegebenenfalls'}
    #text = text.translate(abbreviations_map)

    sentences = re.split('(?<=[\.\?\!\:\,])\s*', text)
    sentences = [sentence for sentence in sentences if len(sentence) >= 2]

    printed_delay = False

    for sentence in sentences:
        wav = tts.tts(text=sentence)

        sounddevice.wait()

        if not printed_delay:
            #print(f"{time.time() - start}s Verzögerung bis zur Antwort.")

            printed_delay = True
            
        sounddevice.play(wav, 22050)

    sounddevice.wait()

say("Sprachausgabedienst bereit für den Einsatz.")

while True:
    try:
        status = requests.get('http://localhost:3000/status').status_code
        
        if status == 200:
            break

        say("Der Spracherkennungsdienst ist nicht mehr erreichbar. Fahre herunter.")
        exit(1)
    except:
        say("Warte auf Spracherkennungsdienst")

say("Spracherkennungsdienst bereit für den Einsatz.")

while True:
    try:
        time.sleep(0.3)

        sentence = requests.get('http://localhost:3000/sentence').text
        sentence_trimmed = sentence.strip()

        if len(sentence_trimmed) == 0:
            continue

        say(sentence_trimmed)

    except:
        say("Der Spracherkennungsdienst ist nicht mehr erreichbar. Fahre herunter.")
        exit(1)