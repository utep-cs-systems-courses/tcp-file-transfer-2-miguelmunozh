#! /usr/bin/env python3

import sys, os
sys.path.append("../lib")       # for params
import re, socket, params
from framedSock import framedSend, framedReceive
from os.path import exists

switchesVarDefaults= (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False),
    )
progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(1)
print("Listening on:", bindAddr)
files_received = []

# accept client requests all the time, create a subprocess for each client request
while True:
    sock, addr = lsock.accept()
    print("\n")
    print(addr, "is connected to server.")
    ####
    try:
        # open file to save data sent through files from the clients
        file = open("Server.txt","w")
        if not os.fork():
            print("new child process handling this client request", addr)

            # keep receiving files from the client
            filename = framedReceive(sock, debug)
            if debug: print("rec'd: ", filename)

            # if server tries to send an empty file
            if filename == None:
                print("Client tried to send an empty or inexistent file!")

            # if the file is already in the server, tell the client
            if filename in files_received:
                # send it to the client
                print("Client tried to send a file that already exists")
                # tell the client about the imaginary file
                framedSend(sock, b"File already exists in server", debug)
            else:
                # add the file received to the list of received files, to check if the file has been sent before
                files_received.append(filename)

                # send to the client the name of the file that the server received
                framedSend(sock,filename,debug)

                print("Server received the following file")
                print(filename)
                print(files_received)
        # close the server.txt file
        file.close()
    except:
        print("Connection to the client lost")
        sys.exit(0)
# close the listener socket
lsock.close()