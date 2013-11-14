#!/usr/bin/env python3
import socket, signal, sys, os

buffsize = 128

def ensure_dir(path):
    if not os.path.exists("recieved"):
        os.makedirs("recieved", 0o777)

def sigterm(signo, sigobj):
    print("SIGTERM: {0} Exitting...".format(signo))
    sys.exit()

def _recieveFile(server, path):
    global buffsize

    ensure_dir(path)    #Create directory

    recieveFile = open("./recieved/" + path, 'wb')
    data = server.recv(buffsize)
    while data != b"":
        recieveFile.write(data)
        data = server.recv(buffsize)

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
    print("Usage: main.py [hostname] <port> <path>")
    sys.exit()
    
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host,port))

except socket.error as msg:
    print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror))
    sys.exit()

server.send(bytes(path, "utf-8"))

_recieveFile(server, path)
server.close()