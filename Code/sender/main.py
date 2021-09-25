from pyzabbix import ZabbixAPI
import sys
import datetime
import time
import argparse
import os
import serial
import hashlib

def calculateHash():
    f = open("data.txt", "rb")
    sha256_hash = hashlib.sha256() #we will calculate the SHA256 of the file to verify integrity.
    line = f.read(1024)
    while line:
        sha256_hash.update(line)
        line = f.read(1024)
    sha256_hash = sha256_hash.digest() #digest transforms into string

    return sha256_hash

def sendFile(ser):
    eof = b'EOF'
    f = open("data.txt","rb")
    print("Starting transfer...")
    ser.flushOutput()
    line = f.read(1024)
    while line:
        ser.write(line)
        line = f.read(1024)
    f.close()
    ser.write(eof)
    ser.flushOutput()
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


def historyToFile(zapi, hosts, items):
    y = 0
    timeTill = int(time.time())
    timeFrom = timeTill- 300
    #in these first lines of code we initialize basic variables for host index counting, and time values(divided 5 minutes apart)

    f = open('data.txt', 'w')

    for item in items:
        hostname = hosts[y]["name"]
        hostid = hosts[y]["hostid"]
        for x in range(len(item)):
            itemkey = item[x]['key_']
            itemid = item[x]['itemid']
            historys = zapi.history.get(hostids = hostid, itemids = itemid, time_from = timeFrom, time_till = timeTill, output="extend")
            for history in historys:
                f.write('"%s" %s %s %s\n' % (hostname, itemkey, history["clock"], history["value"]))
        y+=1
    print('Wxported history...')
    f.close()
    #these loops work in the following way:
        #each item block has the same index of the host,
        #so we take id and name of the host of the specific item block
            #then for each item in the item block we look up it's history, and write it in the file.


#gets items, minimal info to use less system memory, each index of the list is connected to a host with the same index. They are however separate lists.
def getItems(zapi, hosts):
    items = []
    for host in hosts:
        hostid = host['hostid']
        items.append(zapi.item.get(hostids = hostid, output=["key_", "hostid", "hostname"]))
    if len(items) == 0:
        print('No items.. Quitting program')
        sys.exit()
    else:
        print('Items found...')
        return items


#gets host output, minimal info to use less system memory
def getHosts(zapi):
    hosts = zapi.host.get(output=['name'])
    if len(hosts) == 0:
        print('No hosts... Quitting program')
        sys.exit()
    else:
        print('Hosts found...')
        return hosts

#login function, used to get auth key for all Zabbix API calls
def login(zapi, username, password):
    try:
        zapi.login(username, password)
        print ("Login Success...")
    except:
        print ("Zabbix server not reachable... Quitting program")
        sys.exit()

def main():

    #define server
    zapi = ZabbixAPI('http://192.168.1.198/zabbix')

    #log into server
    login(zapi, 'Admin', 'zabbix')

    #recover host list
    hosts = getHosts(zapi)

    #from hosts get items
    items = getItems(zapi, hosts)

    #from items get history and import to file
    historyToFile(zapi, hosts, items)

    #initialize serial port
    ser = createSerial()

    #send file
    sendFile(ser)

    #calculate has from file and send hash value
    hash1 = calculateHash()
    ser.write(hash1)
    print('Hash sent... Closing program.')


if __name__ == '__main__':
    main()
