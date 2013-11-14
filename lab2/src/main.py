#!/usr/bin/env python3
import socket, signal, sys

def sigterm(signo, sigobj):
    print("SIGTERM: {0} Exitting...".format(signo))
    sys.exit()
	
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
    
buffsize = 1024
	
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
    while data != b"":
        client.send(data)
        data = client.recv(buffsize)
    client.close()
