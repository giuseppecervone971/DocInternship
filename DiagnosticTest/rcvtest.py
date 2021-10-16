#!/usr/bin/env python
import time
import serial

#initializing serial port with default parameters
ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

while True:
        x=ser.readline()
        #reads what is being sent via serial port
        print(x)
        #prints it on the console
