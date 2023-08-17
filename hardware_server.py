import serial
import requests

ser = serial.Serial('COM4', 9600, timeout=1)

while True:
    line = str(ser.readline())

    line_split = line.split(' ')

    if len(line_split) != 2:
        continue

    humidity = float(line_split[0][2:])
    temperature = float(line_split[1][:-7])
    print(f"temp: {temperature} humid: {humidity}")

    requests.get(f'http://localhost:3000/set_env?humid={humidity}&temp={temperature}')

ser.close()