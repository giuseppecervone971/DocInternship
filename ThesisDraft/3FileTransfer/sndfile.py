import sys
import datetime
import time
import argparse
import os
import serial
import hashlib

def calculateHash():
    f = open("send/data.txt", "rb")
    sha256_hash = hashlib.sha256() #we will calculate the SHA256 of the file to verify integrity.
    line = f.read(1024)
    while line:
        sha256_hash.update(line)
        line = f.read(1024)
    sha256_hash = sha256_hash.digest() #digest transforms into string

    return sha256_hash

def sendFile(ser):
    eof = b'EOF'
    f = open("send/data.txt","rb")
    print("Starting transfer...")

    line = f.read(512)
    while line:
        ser.write(line)
        line = f.read(512)
    f.close()
    ser.write(eof)

    print('Transfer completed...')

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
#Initialize serial port


def main():

    #initialize serial port
    ser = createSerial()

    #send file
    sendFile(ser)

    #calculate has from file and send hash value
    hash1 = calculateHash()
    time.sleep(5)
    ser.write(hash1)
    print('Hash sent... Closing program.')


if __name__ == '__main__':
    main()
