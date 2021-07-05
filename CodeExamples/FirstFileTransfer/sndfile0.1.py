import serial

ser = serial.Serial(
        port = "/dev/serial0",
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout=1
        )

f = open("log.txt","rb")

line = f.readline
while line:
    ser.write(line)
    line = f.readline

ser.write(b"<<EOF>>")

f.close()

