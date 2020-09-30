#! /usr/bin/env python3

import socket, sys, re
import os.path
from os import path

sys.path.append("../lib") # For params
import params

from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), #boolean (set if present)
    (('-?', '--usage'), "usage", False), #boolean (set if present)
    )

progname = "framedClient" 
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print("Could not open socket...")
    sys.exit(1)

s.connect(addrPort)

# added twice the same file to check for an already existent file in the server side
files = ["file.txt", "file.txt", "file2.txt", "emptyfile.txt", "imaginaryFile.txt"]
sentFiles = []

for file in files:
    # check if the file exists
    if os.path.isfile(file) == False:
        print("The %s file doesnt exist" % file)
    # check if the file is empty
    elif os.path.getsize(file) <= 0:
        print("The file %s is empty!" % file)
    else:
        # check file has been sent already
        if file in sentFiles:
            print("The %s file already exists on the server." % file)
        # send file to the server
        else:
            print("\nSending File %s to Server:" % file)
            framedSend(s, str.encode(file),debug)
            # add file to the list of sent files
            sentFiles.append(file)
            # open file to send content to server
            f  = open(file, "r")
            for line in f:
                framedSend(s, str.encode(line),debug)
                # print contents received from the server
                fr = framedReceive(s,debug)
                print("Server Received: ", fr)
            print("\n")
            f.close()

s.close()