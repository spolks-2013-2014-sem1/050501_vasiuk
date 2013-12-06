#!/usr/bin/env python3
import socket, signal, sys, os, time, fcntl

buffsize = 128
path = ""

def sigterm(signo, sigobj):
    print("SIGTERM: {0} Exitting...".format(signo))
    sys.exit()

def _sendFile(client, addr):
    global buffsize
    global path
    if not os.path.isfile(path):
        print("File " + path + " is not exist")
        return

    print(bytes(str(os.stat(path).st_size), "utf-8"))
    client.sendto(bytes(str(os.stat(path).st_size), "utf-8"), addr)
    time.sleep(0.001)
    
    sendFile = open(path, 'rb')
    sentData = 0

    data = sendFile.read(buffsize)
    while data != b"":
        client.sendto(data, addr)
        sentData += len(data)
        data = sendFile.read(buffsize)
        time.sleep(0.001)

signal.signal(signal.SIGTERM, sigterm)
signal.signal(signal.SIGINT, sigterm)

if len(sys.argv) == 4:
    host = sys.argv[1]
    port = int(sys.argv[2])
    path = sys.argv[3]
elif len(sys.argv) == 3:
    host = "localhost"
    port = int(sys.argv[1])
    path = sys.argv[2]
else:
    print("Usage: clientn.py [hostname] <port> <filepath>")
    sys.exit()

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #option for force socket reusing

except socket.error as msg:
    print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror))
    sys.exit()

addr = (host, port)

server.sendto(bytes(os.path.basename(path), "UTF-8"), addr)
time.sleep(0.001)
_sendFile(server, addr)
server.close()