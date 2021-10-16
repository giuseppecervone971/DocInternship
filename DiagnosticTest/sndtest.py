#!/usr/bin/env python
import time
import serial

#initializing serial port with default parameters
ser = serial.Serial(
        port='/dev/serial0', 
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

counter=0 

while True:
        ser.write(b'Write counter: %d \n'%(counter)) #write in byte form what to send on the serial port
        time.sleep(1)
        counter += 1
