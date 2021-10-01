import serial
import time
import hashlib
import subprocess

#this function is what we use to send the data to the trapper items in zabbix.
def sender():
    f = open("/home/pi/DocInternship/rcv/data.txt", "r")
    #the 
    line = f.readline()
    while line: #zabbix sender takes 250 values at the time, so we split the data.txt file in small 250lines tmp files.
        x = 0
        f2 = open("/home/pi/DocInternship/rcv/tmp.txt", "w")
        while x in range(250):
            f2.write(line)
            line = f.readline()
            x+=1
        f2.close()
        subprocess.run(["zabbix_sender", "-z", "192.168.1.157", "-i", "/home/pi/DocInternship/rcv/tmp.txt", "-T", "-vv"])


def calculateHash():
    f = open("/home/pi/DocInternship/rcv/data.txt", "rb")
    sha256_hash = hashlib.sha256()
    line = f.read(1024)
    while line:
        sha256_hash.update(line)
        line = f.read(1024)
    sha256_hash = sha256_hash.digest()
    
    return sha256_hash


def recvHash(ser):
    while True:
        if ser.inWaiting() < 32: #SHA256 hash is 32 bytes long
            time.sleep(1)
        else:
            break
    hash2 = ser.read(32)
    return hash2


def recvFile(ser):
    eof = b'EOF'
    f = open("/home/pi/DocInternship/rcv/data.txt", "wb")
    
    while True:
        recvdatalen = ser.inWaiting()
        if recvdatalen>0:
            line = ser.read(recvdatalen)
            #The idea is that we only ever read from the serial port the bytes we see, limiting the probability of taking a chunk of SHA256 hash. 
            if eof in line:
                f.write(line[:-3]) #once the chunk has EOF, write to file removing the 3 EOF bytes
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
