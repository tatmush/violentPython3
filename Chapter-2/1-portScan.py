#!/usr/bin/python
import argparse
from socket import *
from threading import *

screenLock=Semaphore(value=1)

def connScan(tgtHost, tgtPort):
    try:
        connSkt=socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send(b'ViolentPython\r\n')
        results=connSkt.recv(100)
        screenLock.acquire()
        print('[+] {} tcp open'.format(tgtPort))
        print('[+] {}'.format(str(results, 'utf-8')))

    except:
        screenLock.acquire()
        print('[-] {} tcp closed'.format(tgtPort))

    finally:
        screenLock.release()
        connSkt.close()

def portScan(tgtHost, tgtPorts):
    try:
        tgtIp=gethostbyname(tgtHost)
        
    except:
        print('[-] Cannot resolve {}, Unknows host'.format(tgtHost))
        return
    try:
        tgtName=gethostbyaddr(tgtIp)
        print('[+] Scan results for: {}'.format(tgtName[0]))
    except:
        print('[+] Scan resutls for: {}'.format(tgtIp))
    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t=Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()

def main():
    parser=argparse.ArgumentParser(description='usage -H <target  host> -p "<target port>"')
    parser.add_argument('-H', dest='tgtHost', type=str, help='specify the target host')
    parser.add_argument('-p', dest='tgtPort', type=str, help='specify the target port[s] separated by a comma')
    args=parser.parse_args()
    tgtHost=args.tgtHost
    tgtPorts=str(args.tgtPort).split(', ')
    if (tgtHost==None) and (tgtPorts[0]==None):
        print(parser.usage)
        exit(0)
    portScan(tgtHost, tgtPorts)

if __name__=='__main__':
    main()
        
