#!/usr/bin/env python3
import socket, signal, sys, os

buffsize = 128

def sigterm(signo, sigobj):
    print("SIGTERM: {0} Exitting...".format(signo))
    sys.exit()

def _sendFile(client, path):
    global buffsize
    if not os.path.isfile(path):
        print("File " + path + " is not exist")
        return
    sendFile = open(path, 'rb')
    data = sendFile.read(buffsize)
    while data != b"":
        client.send(data)
        data = sendFile.read(buffsize)

signal.signal(signal.SIGTERM, sigterm)
signal.signal(signal.SIGINT, sigterm)

if len(sys.argv) == 3:
    host = sys.argv[1]
    port = int(sys.argv[2])
elif len(sys.argv) == 2:
    host = "localhost"
    port = int(sys.argv[1])
else:
    print("Usage: main.py [hostname] <port>")
    sys.exit()
    
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #option for force socket reusing
    server.bind((host,port))

except socket.error as msg:
    print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror))
    sys.exit()

server.listen(5)

while True:
    client, address = server.accept()
    data = client.recv(buffsize)
    _sendFile(client, "./files/" + data.decode("utf-8"))
    client.close()
