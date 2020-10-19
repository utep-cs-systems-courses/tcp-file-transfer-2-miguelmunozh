#! /usr/bin/env python3

import socket, sys, re, os
sys.path.append("../lib") # For params


from encapFramedSock import EncapFramedSock


addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = ("127.0.0.1", 50001)

s = socket.socket(addrFamily, socktype)

if s is None:
    print("Could not open socket...")
    sys.exit(1)

s.connect(addrPort)
fsock = EncapFramedSock((s, addrPort))




# file passed as argument
file = sys.argv[1]

# check if the file exists
if os.path.isfile(file) == False:
    print("The %s file doesnt exist" % file)

# check if the file is empty
elif os.path.getsize(file) <= 0:
    print("The file %s is empty!" % file)
else:
    print("\nFile %s sent to Server" % file)
    fsock.send(str.encode(file))

    # # open file to send content to server
    f  = open(file, "r")
    for line in f:
        fsock.send(str.encode(line))
    print("\n")
    f.close()
    # get response from server
    content = fsock.receive()
    print(content)

s.close()