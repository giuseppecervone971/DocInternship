import serial
import time
import os
from hurry.filesize import size,alternative
import hashlib

ser = serial.Serial(
        port = "/dev/serial0",
        baudrate = 115200,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout=1
        )
#Initialize serial port

filesize = size(os.path.getsize('log.txt'), system=alternative)
#gets filesize in a nice manner to read, will be used for performance purposes

sha256_hash = hashlib.sha256()
#we will calculate the SHA256 of the file to verify integrity.

f = open("log.txt","rb")
print("Starting transfer... Time started")
start_time= time.time()
#Here we open the file, and keep on reading until there's lines
#we then send <<EOF>> to signal to the other machine that file transfer is over.
ser.flushOutput()
line = f.readline()
while line:
    sha256_hash.update(line)
    ser.write(line)
    line = f.readline()
end_time = time.time() - start_time
f.close()
ser.write(b"<<EOF>>\n")

sha256_hash = sha256_hash.digest() #digest transforms into string
ser.write(sha256_hash)


print('Transfer completed... Filesize:',filesize,'. Time:',end_time,'seconds.')
