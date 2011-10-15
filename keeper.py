#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  Copyright (C) 2011 Yann GUIBET <yannguibet@gmail.com>
#  See LICENSE for details.

import sys, os
from getpass import getpass
from getpwd import getpwd
from hashlib import sha256, sha512
from base64 import b64encode, b64decode
from Index import Index
from Crypto import *
from Config import *

class shell():
    commands = {
        "help" : "for help :)",
        "exit" : "To exit ;)",
        "index" : "...",
        "add_data" : "...",
        "rm_data" : "...",
        "show" : "...",
        "clear" : "...",
        "update_key" : "...",
        }

    def __init__(self):
        self.db = Index(shadow)
        try:
            self.key = getpass('password : ')
        except Exception:
            raise Exception("getpwd fail ...")

    def loop(self):
        while True:
            try:
                buffer = self._input('\n> ')
                if buffer == "exit":
                    return
                elif buffer in self.commands:
                    eval("self.%s()" % buffer)
                else:
                    print("Command not found")
            except Exception as e:
                print(e)

    def _input(self, msg):
        sys.stdout.write(msg)
        sys.stdout.flush()
        return sys.stdin.readline().replace('\n','')

    def help(self):
        for i in self.commands:
            print(i,":",self.commands[i])

    def index(self):
        all = self.db.get_all()
        print("\nDatas :")
        if all == []:
            print(">> None")
        for i in all:
            ctx = aes(self.key, b64decode(i[2].encode()), 0, 'cbc')
            plain = ctx.ciphering(b64decode(i[1].encode()))
            if sha512(plain).digest() != b64decode(i[3].encode()):
                raise Exception("Fail to decrypt %d" % i[0])
            j = plain.find(b'\0')
            print(str(i[0])+") "+plain[:j].decode()+" : "+i[2])

    def show(self):
        id = int(self._input("ID : "))
        data = self.db.get_data_by_id(id)
        ctx = aes(self.key, b64decode(data[2].encode()), 0, 'cbc')
        plain = ctx.ciphering(b64decode(data[1].encode()))
        if sha512(plain).digest() != b64decode(data[3].encode()):
            raise Exception("Fail to decrypt %d" % data[0])
        j = plain.find(b'\0')
        print(">> "+plain[:j].decode()+" : "+plain[j+1:].decode())
        self._input("\nPress [enter] to clean ...")
        self.clear()

    def add_data(self):
        name = self._input('name : ')
        plain = self._input('data : ')
        iv = os.urandom(16)
        ctx = aes(self.key, iv, 1, 'cbc')
        buff = name+'\0'+plain
        self.db.add_data(ctx.ciphering(buff.encode()), iv, sha512(buff.encode()).digest())
        self.clear()
        print(">> SUCCESS")

    def rm_data(self):
        id = int(self._input('ID : '))
        self.db.rm_data(id)
        print(">> SUCCESS")

    def update_key(self):
        oldkey = getpass('old password : ')
        if oldkey != self.key:
            raise Exception("Bad Key ...")
        newkey = getpass('new password : ')
        if newkey != getpass('retype new password : '):
            raise Exception("Password doesn't match ...")
        print("Update encryption key. Please wait ...")
        from xml.dom.minidom import parseString
        xml = parseString(self.db.get_xml())
        index = xml.getElementsByTagName("data")
        for i in index:
            data = b64decode(i.getAttribute("data"))
            iv = b64decode(i.getAttribute("iv"))
            hash = b64decode(i.getAttribute("hash"))
            ctx = aes(self.key, iv, 0, 'cbc')
            data = ctx.ciphering(data)
            if sha512(data).digest() != hash:
                raise Exception("FAIL to decrypt %d ..." % i.getAttribute("id"))
            iv = os.urandom(16)
            ctx = aes(newkey, iv, 1, 'cbc')
            data = ctx.ciphering(data)
            i.setAttribute("data", b64encode(data))
            i.setAttribute("iv", b64encode(iv))
        self.key = newkey
        self.db.set_xml(xml.toxml())
        
    def clear(self):
        os.system('clear')

def main():
    try:
        S = shell()
        print("try help for help ;)")
        S.loop()
    except Exception as e:
        raise
        print(e)
        pass
    except KeyboardInterrupt:
        print("Bye")
    else: 
        print("Bye")
    sys.exit(0)

if __name__ == '__main__':
    main()
