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

eof = '<<EOF>>'

f = open("log.txt", "w")

x = ser.readline()
x = x.deecode()

while x != eof:
    f.write(x)
    x = ser.readline()
    x = x.decode()
f.close()
