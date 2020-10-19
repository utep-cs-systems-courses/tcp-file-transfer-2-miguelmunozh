#! /usr/bin/env python3

import sys
import time
sys.path.append("../lib")  # for params
import re, socket, params, os
from encapFramedSock import EncapFramedSock

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
lsock.listen(5)
print("listening on:", bindAddr)

from threading import Thread, Lock

lock = Lock()


class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)


    def run(self):
        # time.sleep(4)
        print("\nNew thread handling connection from", self.addr)
        # lock the critical section for threads
        lock.acquire()
        # get file sent by client
        payload = self.fsock.receive(debug)
        if debug:
            print("rec'd: ", payload)
        # if nothing is sent, release the lock
        if not payload:
            print("Client tried to send an empty file or an unexistent file")
            # close the socket
            self.fsock.close()
            lock.release()
            sys.exit(1)

        name = payload.decode()

        try:
            # if it doesnt exist in server, create the file and write its contents to it
            if not os.path.isfile(name):
                # create a file and write the content of the sent file to it
                content = self.fsock.receive(debug)

                file = open(name, 'wb+')
                file.write(content)
                file.close()

                print("Received file", name)
                # send info back to the client
                self.fsock.send(b"File has been received by the server", debug)

            else:
                print("The File with name", name, "already exists on server.")
                # send info back to the client
                self.fsock.send(b"File already exists on th server", debug)


        except FileNotFoundError:
            print("File wasnt found")
        lock.release()
        self.fsock.close()

# keep making threads for the up comming clients
while True:
    # if a client tries to connect to the sserver make a thread for that client and start it
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()