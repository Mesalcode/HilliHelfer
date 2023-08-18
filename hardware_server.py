import serial
import requests

ser = serial.Serial('COM4', 9600, timeout=1)

while True:
    line = str(ser.readline())

    line_split = line.split(' ')

    if len(line_split) != 2:
        continue

    try:
        humidity = float(line_split[0][2:])
        temperature = float(line_split[1][:-7])
    except:
        continue
    print(f"temp: {temperature} humid: {humidity}")

    response_text = requests.get(f'http://localhost:3000/set_env?humid={humidity}&temp={temperature}').text
    response_text_split = response_text.split(' ')

    if len(response_text_split) != 2:
        continue

    print(response_text_split)

    lightEnabled = int(response_text_split[0])
    fanEnabled = int(response_text_split[1])

    print((lightEnabled, fanEnabled))

    ser.write(f'{lightEnabled}{fanEnabled}\r'.encode())

ser.close()