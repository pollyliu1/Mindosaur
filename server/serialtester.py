# import serial
# comport = 'COM5'

import serial
import time
arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)

while True:
    arduino.write(bytes("2", 'utf-8'))
    time.sleep(1)