import serial

ser = serial.Serial('COM4', 9600, timeout=1)

while True:
    line = str(ser.readline())

    line_split = line.split(' ')

    if len(line_split) != 2:
        continue

    temperature = float(line_split[0][2:])
    humidity = float(line_split[1][:-2])
    print(f"temp: {temperature} humid: {humidity}")

ser.close()