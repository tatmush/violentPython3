#!/usr/bin/python

import crypt

def testPass(cryptPass):
    salt=cryptPass[0:2]
    with open('dictionary.txt', 'r') as dictFile:
        for word in dictFile.readlines():
            word=word.strip('\n')
            cryptWord=crypt.crypt(word,salt)
            if(cryptWord==cryptPass):
                print('[+] Found Password: {}'.format(word))
                return
        print('[-] Password not found')
        return

def main():
    with open('passwords.txt') as passFile:
        for line in passFile.readlines():
            if':' in line:
                user=line.split(':')[0]
                cryptPass=line.split(':')[1].strip(' ')
                print('[*] Cracking password for: {}'.format(user))
                testPass(cryptPass)

if __name__=='__main__':
    main()
