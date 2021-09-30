import serial
import time
import hashlib
import subprocess

def sender():
    f = open("/home/pi/rcv/data.txt", "r")
    line = f.readline()
    while line:
        x = 0
        f2 = open("/home/pi/rcv/tmp.txt", "w")
        while x in range(250):
            f2.write(line)
            line = f.readline()
            x+=1
        f2.close()
        subprocess.run(["zabbix_sender", "-z", "192.168.1.157", "-i", "tmp.txt", "-T", "-vv"])


def calculateHash():
    f = open("/home/pi/rcv/data.txt", "rb")
    sha256_hash = hashlib.sha256()
    line = f.read(1024)
    while line:
        sha256_hash.update(line)
        line = f.read(1024)
    sha256_hash = sha256_hash.digest()
    
    return sha256_hash


def recvHash(ser):
    while True:
        if ser.inWaiting() < 32:
            time.sleep(1)
        else:
            break
    hash2 = ser.read(32)
    return hash2


def recvFile(ser):
    eof = b'EOF'
    f = open("/home/pi/rcv/data.txt", "wb")

    while True:
        recvdatalen = ser.inWaiting()
        if recvdatalen>0:
            line = ser.read(recvdatalen)
            if eof in line:
                f.write(line[:-3])
                break
            else:
                f.write(line)
        time.sleep(0.001)
    print("File transfer completed...")


def createSerial():
    try:
        ser = serial.Serial(
            port = "/dev/ttyUSB0",
            baudrate = 115200,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 1
        ) #initialize serial port
        print("Serial port created...")
        return ser
    except Exception as e:
        print(e)


def main():
    
    #create serial port
    ser = createSerial()

    while True:
        #receive file
        recvFile(ser)

    #receive hash in sha256 form
        hash2 = recvHash(ser)

    #calculate hash from received file
        hash1 = calculateHash()

    #if the two hash values are equal, file transfer successful, else file transfer failed.
        if hash1==hash2:
            print("File Transfer Success... Importing data in Zabbix...")
            sender()
            print("File imported...")
        else:
            print("File Transfer Failed")




if __name__ == '__main__':
    main()
