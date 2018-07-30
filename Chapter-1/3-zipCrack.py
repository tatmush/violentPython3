#!/usr/bin/python

import zipfile
import argparse
import threading

def extractFile(zFile, password):
    try:
        zFile.extractall(pwd=password)
        print('[+] Found password: {}'.format(str(password, 'utf-8')))
    except:
       pass

def main():
    parser=argparse.ArgumentParser(description='Perform a dictionary attack on an excrypted zip file')
    parser.add_argument('-f', dest='zname', type=str, help='specify zip file')
    parser.add_argument('-d', dest='dname', type=str, help='specify dictionary file')
    args=parser.parse_args()

    #BUG: when no args passed. Should print usage
    if (args.zname==None) or (args.dname==None):
        print(parser.usage)
        exit(0)
        
    else:
        zname=args.zname
        dname=args.dname

    zFile=zipfile.ZipFile(zname)
    with open(dname) as passFile:
        for line in passFile.readlines():
            password=bytes(line.strip('\n'), 'utf-8')
            t=threading.Thread(target=extractFile, args=(zFile, password))
            t.start()
            
if __name__=='__main__':
        main()
    
