from pyzabbix import ZabbixAPI
import sys
import datetime
import time
import argparse
import os

def exportToCSV(historys, itemkey, hosts):
    f = open(data.txt, 'w')
    for history in historys:
        f.write('"%s" %s %s %s\n' % (hostname, itemkey, timestamp, history["value"])) 
    print('exported history')
    f.close()

def getItems(zapi, hosts):
    for host in hosts:
        listname = host[0] ##diamo il nome dell'host come lista. ogni host avra una lista con il suo nome e tutti i suoi oggetti
        print(listname)
        listname = []
        listname.append(items = zapi.item.get(hostname = host[0], output=['key']))
    
    

def getHosts(zapi):
    hosts = zapi.host.get(output=['name'])
    return hosts


def login(zapi, username, password):
    try:
        zapi.login(username, password)
        print ("login succeed.")
    except:
        print ("zabbix server is not reachable: ")
        sys.exit()


def main():
    
    #define server
    zapi = ZabbixAPI('http://192.168.1.198/zabbix')
    
    #log into server
    zapi.login(zapi, 'Admin', 'zabbix')
    
    #get hosts
    hosts = getHosts(zapi)
    
    getItems(zapi, hosts)
    #from hosts get items




if __name__ == '__main__':
    main()
