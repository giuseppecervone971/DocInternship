import serial
import time
import hashlib

ser = serial.Serial(
        port = "/dev/ttyUSB0",
        baudrate = 19200,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
        )
#initialize serial port

eof = b"<<EOF>>\n"
#define EOF, signals to the receiver that the file is over

sha256_hash = hashlib.sha256() #we will calculate the SHA256 of the file to verify it's integrity after transfering

f = open("log.txt", "wb") #open file to write into

x = ser.readline()
while x != eof: #until file comes, decode, if x=eof then check if file transfered correctly
    sha256_hash.update(x) #decoding is done in bytes, so we make sha before making it in bits
    f.write(x)
    x = ser.readline()
f.close()

sha256_send = ser.read(32)
if sha256_send != sha256_hash.digest():
    print("File Transfer failed")
else:
    print("File Transfer success")
