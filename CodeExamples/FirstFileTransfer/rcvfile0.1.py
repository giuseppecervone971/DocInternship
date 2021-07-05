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

filestart = '<<FILE START>>'
eof = '<<EOF>>'

f = open("log.txt", "w")

x = ser.readline()
x = x.deecode()

while x != eof and x != filestart:
    if x != eof and x != filestart:
        x = ser.readline()
        x = x.decode()
        f.write(x)
f.close()
