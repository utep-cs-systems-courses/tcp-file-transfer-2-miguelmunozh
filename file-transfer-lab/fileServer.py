#! /usr/bin/env python3

import sys
import re, socket, params

sys.path.append("../lib") # For params

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
print("Waiting for connection...")

sock, addr = lsock.accept()
print(addr, "is connected to server.")

from framedSock import framedSend, framedReceive

####
# open file to save data sent through files from the clients
file = open("Server.txt","w")
files_received = []
while True:
    # keep receiving files from the client
    filename = framedReceive(sock, debug)
    # add the file received to the list of received files
    files_received.append(filename)
    # write the name of the file to the server.txt
    file.write("Contents of %s\n" % filename)

    # get payload from file comming from the client
    payload = framedReceive(sock, debug)
    if debug: print("rec'd: ", payload)
    if not payload:
        break
    # write the contents of the file to the server.txt file on the server side
    content = payload.decode("utf-8")
    file.write("'%s'\n" % content)
    # send to the client the contents of the file that the server received
    framedSend(sock,payload,debug)

print("Server received the following files")
for x in files_received:
    print(x)
# close the server.txt file
file.close()
# close the listener socket
lsock.close()