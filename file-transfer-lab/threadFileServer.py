#! /usr/bin/env python3

import sys

sys.path.append("../lib")  # for params
import re, socket, params, os

sys.path.append("../framed-echo")
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(1)

from threading import Thread, Lock

lock = Lock()


class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        print("listening on:", bindAddr)


    def run(self):
        print("\nnew thread handling connection from", self.addr)
        
        lock.acquire()
        # get file name
        payload = framedReceive(self.sock, debug)
        if debug:
            print("rec'd: ", payload)
        # if nothing is sent
        if not payload:
            lock.release()
            sys.exit(1)

        payload = payload.decode()

        name = payload
        content = payload.encode()

        try:
            # if it doesnt exist in server, create the file and write its contents to it
            if not os.path.isfile(name):
                # create a file and write the content of the sent file to it
                file = open(name, 'wb+')
                file.write(content)
                file.close()

                print("Received file", payload)
            else:
                print("The File with name", name, "already exists on server.")
        except FileNotFoundError:
            print("File wasnt found")
        lock.release()


while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()