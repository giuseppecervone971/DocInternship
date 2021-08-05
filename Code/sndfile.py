import serial
import time
import os
from hurry.filesize import size,alternative
import hashlib


def calculateHash():
    f - open("log.txt", "rb")
    sha256_hash = hashlib.sha256()
    line = f.read(2048)
    while line:
        sha256_hash.update(line)
        line = f.read(2048)
    sha256_hash = sha256_hash.digest()

    return sha256_hash

def sendFile(ser):
    eof = b'EOF'

    f = open("log.txt", "rb")
    print("Starting transfer.. Time started")
    ser.flushOutput()
    line = f.read(2048)
    while line:
        ser.write(line)
        line = f.read(2048)
    f.close()
    ser.write(eof)
    ser.flushOutput()


def createSerial():
    try:
        ser = serial.Serial(
            port = "/dev/serial0",
            baudrate = 115200,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout=1
            )
        return ser
    except Exception as e:
        print(e)

def main():

    filesize = size(os.path.getsize('log.txt'), system = alternative)
    
    ser = createSerial()

    start_time = time.time()
    sendFile(ser)
    end_time = time.time()-start_time
    print('Transfer completed... Filesize:',filesize,'. Time:',end_time,'seconds.')

    hash1 = calculateHash()
    ser.write(hash1)
    print('Hash sent')


if __name__ == '__main__':
    main()
