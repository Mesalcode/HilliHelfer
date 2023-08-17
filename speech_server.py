print("hallo")

from TTS.api import TTS
import sounddevice
print("1")
import regex as re
import time
print("2")
import requests
print("3")

reply_server_url = "https://calm-flies-appear.loca.lt"
speech_server_url = "https://calm-flies-appear.loca.lt"
communication_server_url = "http://localhost"

tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC")


print("test")

def say(text, notify_others=False):
    text.replace("\"", "")
    text.replace("'", "")

    if notify_others:
        requests.get(f'{speech_server_url}/pause')

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
        requests.get(f'{speech_server_url}/unpause')

say("Alle Systeme werden vor dem Start überprüft. Bitte haben Sie etwas Geduld.")

say("Sprachausgabedienst bereit für den Einsatz.")

while True:
    try:
        status = requests.get(f'{speech_server_url}/status').status_code
        
        if status == 200:
            break   

        print(status)

        say("Der Spracherkennungsdienst ist nicht mehr erreichbar. Fahre herunter.")
        exit(1)
    except Exception as e:
        print(e)
        say("Warte auf Spracherkennungsdienst")

say("Spracherkennungsdienst bereit für den Einsatz.")

while True:
    try:
        status = requests.get(f'{communication_server_url}:3002/status').status_code
        
        if status == 200:
            break   

        say("Der Kommunikationsdienst ist nicht mehr erreichbar. Fahre herunter.")
        exit(1)
    except:
        say("Warte auf Kommunikationsdienst")

say("Kommunikationsdienst bereit für den Einsatz.")

say("Starte Hilli punkt echse")

time.sleep(5)

say("Guten Tag! Ich bin Thomas Hillebrand, Gymnasiallehrer aus dem steinreichen Lindlar und freue mich mit dir zu reden.")

while True:
    try:
        time.sleep(0.3)

        print("sending request")

        sentence = requests.get(f'{speech_server_url}/sentence').text
        sentence_trimmed = sentence.strip()

        print(sentence)


        if len(sentence_trimmed) == 0:
            continue

        print(f"Erkannte Sprache: {sentence_trimmed}")

        lower_case_sentence = sentence_trimmed.lower()
        thomas_index = lower_case_sentence.find("thomas")

        if thomas_index == -1:
            continue

        thomas_sentence = sentence[thomas_index:]
        trimmed_thomas_sentence = thomas_sentence.strip()

        if len(trimmed_thomas_sentence) == 0:
            continue

        print(f"Looking for response to {trimmed_thomas_sentence}")

        reply = requests.post('f{communication_server_url}:3002/get_response', json={'query': trimmed_thomas_sentence}).text

        environment_values = requests.get(f'{speech_server_url}/get_env').json()

        reply.replace("%humid%", environment_values['humidity'])
        reply.replace("temp%", environment_values['temperature'])

        #print(environment_values)

        say(reply, notify_others=True)
    except Exception as e:
        print(e)

        say("Der Spracherkennungsdienst ist nicht mehr erreichbar. Fahre herunter.")
        exit(1)

# TODO: Spracherkennung sendet Hardware signal für lampe