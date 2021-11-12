import serial
import time
import os
from hurry.filesize import size,alternative

ser = serial.Serial(
        port = "/dev/serial0",
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout=1
        )
#Initialize serial port

filesize = size(os.path.getsize('log.txt'), system=alternative)
#gets filesize in a nice manner to read,
#will be used for performance purposes

print("Starting transfer... Time started")
start_time= time.time()
#Here we open the file, and keep on reading until there's
#lines, we then send <<EOF>> to signal to the other
#machine that file transfer is over.

f = open("log.txt","rb")
line = f.readline()
while line:
    ser.write(line)
    line = f.readline()

ser.write(b"<<EOF>>\n")

f.close()

end_time = time.time() - start_time

print('Transfer completed... Filesize:',filesize,'. Time:',end_time,'seconds.')
