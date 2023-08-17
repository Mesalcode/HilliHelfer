import serial

ser = serial.Serial('COM4', 9600, timeout=1)

while True:
    line = ser.readline()

    print(line)

ser.close()