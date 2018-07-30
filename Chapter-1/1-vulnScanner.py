#!/usr/bin/python

import socket
import os
import sys

def retBanner(ip, port):
    
    try:
        socket.setdefaulttimeout(2)
        s=socket.socket()
        s.connect((ip, port))
        banner=s.recv(1024)
        banner=str(banner, 'utf-8')
        return banner
    except:
        return

def checkVulns(banner, filename):
    
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line.strip('\n') in banner:
                print('[+] Server is vulnerable: {}'.format(str(banner).strip('\n')))

def main():
    
    if len(sys.argv)==2:
        
        filename=sys.argv[1]
        if not os.path.isfile(filename):
            print('[-] {} does not exist'.format(filename))
            exit(0)

        if not os.access(filename, os.R_OK):
            print('[-] {} access denied'.format(filename))
            exit(0)

    else:
        print('[-] Usage: {} <vuln filename>'.format(sys.argv[0]))
        exit(0)

    portList=[21,22,25,80,110,443]
    for x in range(147, 150):
        ip='192.168.100.' + str(x)
        for port in portList:
            banner=retBanner(ip, port)
            if banner:
                print('[+] {} : {}'.format(ip, banner))
                checkVulns(banner, filename)
                
if __name__=='__main__':
    main()
    

                
