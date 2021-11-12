import serial
import time

ser = serial.Serial(
        port = "/dev/ttyUSB0",
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
        )

eof = b'<<EOF>>\n'

f = open("log.txt", "wb")

x = ser.readline()

while x != eof:
    f.write(x)
    x = ser.readline()
f.close()
