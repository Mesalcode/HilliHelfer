print("hallo")

from TTS.api import TTS
import sounddevice
print("1")
import regex as re
import time
print("2")
import requests
print("3")

speech_server_url = "https://rnyyh-80-153-191-202.a.free.pinggy.online"
communication_server_url = "http://localhost:3002"

tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC")


print("test")

def say(text, notify_others=False):
    clean_text = text

    text = text.replace("\"", "")
    text = text.replace("'", "")

    if notify_others:
        requests.get(f'{speech_server_url}/pause')

    start = time.time()

    special_char_map = {ord('ä'):'ae', ord('Ä'):'Ae', ord('ü'):'ue', ord('Ü'):'Ue', ord('ö'):'oe', ord('Ö'):'Oe', ord('ß'):'ss'}
    text = text.translate(special_char_map)

    #abbreviations_map = {'bzw.': 'beziehungsweise', 'usw.': 'und so weiter', 'bzgl.':'bezüglich', 'ggf': 'gegebenenfalls'}
    #text = text.translate(abbreviations_map)

    sentences = re.split('(?<=[\.\?\!\:\,])\s*', text)
    sentences = [sentence for sentence in sentences if len(sentence) >= 2]

    text = ' '.join(sentences)

    printed_delay = False

    for sentence in sentences:
        wav = tts.tts(text=sentence)

        sounddevice.wait()

        if not printed_delay:
            #print(f"{time.time() - start}s Verzögerung bis zur Antwort.")
            requests.post(f'{speech_server_url}/set_bubble_text', json={'text': clean_text})
            requests.get(f'{speech_server_url}/disable_thinking_bubble')
            printed_delay = True
            
        sounddevice.play(wav, 22050)

    sounddevice.wait()

    if notify_others:
        requests.get(f'{speech_server_url}/unpause')

#say("Alle Systeme werden vor dem Start überprüft. Bitte haben Sie etwas Geduld.")

#say("Sprachausgabedienst bereit für den Einsatz.")

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

#say("Spracherkennungsdienst bereit für den Einsatz.")

while True:
    try:
        status = requests.get(f'{communication_server_url}/status').status_code
        
        if status == 200:
            break   

        say("Der Kommunikationsdienst ist nicht mehr erreichbar. Fahre herunter.")
        exit(1)
    except:
        say("Warte auf Kommunikationsdienst")

#say("Kommunikationsdienst bereit für den Einsatz.")

#say("Starte Hilli punkt echse")

#time.sleep(5)

say("Guten Tag! Ich bin Thomas Hillebrand, Gymnasiallehrer aus dem steinreichen Lindlar und freue mich mit dir zu reden.", notify_others=True)

DEBUG_MODE = False

while True:
    try:
        time.sleep(0.3)

        print("sending request")

        if DEBUG_MODE: 
            sentence = input("Eingabe: ")
        else:
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
        requests.get(f'{speech_server_url}/enable_thinking_bubble')

        reply = requests.post(f'{communication_server_url}/get_response', json={'query': trimmed_thomas_sentence}).text

        environment_values = requests.get(f'{speech_server_url}/get_env').json()

        reply = reply.replace("%humid%", str(environment_values['humidity']).replace('.', ' komma '))
        reply = reply.replace("%temp%", str(environment_values['temperature']).replace('.', ' komma '))

        if ('%lighton%' in reply):
            requests.get(f'{speech_server_url}/enable_light')
        

        if ('%lightoff%' in reply):
            requests.get(f'{speech_server_url}/disable_light')
        

        if ('%fanon%' in reply):
            requests.get(f'{speech_server_url}/enable_fan')
        

        if ('%fanoff%' in reply):
            requests.get(f'{speech_server_url}/disable_fan')
        

        reply = reply.replace('%lighton%', '🔋')
        reply = reply.replace('%lightoff%', '🪫')

        reply = reply.replace('%fanon%', '🔋')
        reply = reply.replace('%fanoff%', '🪫')

        #print(environment_values)

        say(reply, notify_others=True)
    except Exception as e:
        print(e)

        say("Ein kritischer Fehler ist aufgetreten. Fahre herunter.")
        exit(1)

# TODO: Spracherkennung sendet Hardware signal für lampe