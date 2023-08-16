print("hallo")

from TTS.api import TTS
import sounddevice
print("1")
import regex as re
import time
print("2")
import requests
print("3")

tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False, gpu=False)

print("test")

def say(text, notify_others=False):
    if notify_others:
        requests.get('http://localhost:3000/pause')

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

    if notify_others:
        requests.get('http://localhost:3000/unpause')

say("Alle Systeme werden vor dem Start überprüft. Bitte haben Sie etwas Geduld.")

while True:
    try:
        print("vordere ")

        status = requests.get('http://localhost:3000/status').status_code
        
        if status == 200:
            break   

        say("Der Spracherkennungsdienst ist nicht mehr erreichbar. Fahre herunter.")
        exit(1)
    except:
        say("Warte auf Spracherkennungsdienst")

say("Guten Tag! Ich bin Thomas Hillebrand, Gymnasiallehrer aus dem steinreichen Lindlar und freue mich mit dir zu reden.")

while True:
    try:
        time.sleep(0.3)

        sentence = requests.get('http://localhost:3000/sentence').text
        sentence_trimmed = sentence.strip()

        if len(sentence_trimmed) == 0:
            continue

        lower_case_sentence = sentence_trimmed.lower()
        thomas_index = lower_case_sentence.find("thomas")

        if thomas_index == -1:
            continue

        thomas_sentence = sentence[thomas_index:]
        trimmed_thomas_sentence = thomas_sentence.strip()

        if len(trimmed_thomas_sentence) == 0:
            continue

        print(thomas_sentence)

        say(thomas_sentence, notify_others=True)

    except:
        say("Der Spracherkennungsdienst ist nicht mehr erreichbar. Fahre herunter.")
        exit(1)