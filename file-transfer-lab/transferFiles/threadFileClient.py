#! /usr/bin/env python3

import socket, sys, re, os
sys.path.append("../lib") # For params


from framedSock import framedSend, framedReceive


addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = ("127.0.0.1", 50001)

s = socket.socket(addrFamily, socktype)

if s is None:
    print("Could not open socket...")
    sys.exit(1)

s.connect(addrPort)

# file passed as arguments
file = sys.argv[1]

# check if the file exists
if os.path.isfile(file) == False:
    print("The %s file doesnt exist" % file)
    #framedSend(s, str.encode("imaginary file received"))

# check if the file is empty
elif os.path.getsize(file) <= 0:
    print("The file %s is empty!" % file)
else:
    print("\nSending File %s to Server:" % file)
    framedSend(s, str.encode(file))

    # # open file to send content to server
    # f  = open(file, "r")
    # for line in f:
    #     framedSend(s, str.encode(line))
    #     # print contents received from the server
    #     fr = framedReceive(s)
    #     print("Server : ", fr)
    # print("\n")
    # f.close()

s.close()