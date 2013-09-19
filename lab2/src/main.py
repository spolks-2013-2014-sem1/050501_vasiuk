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
    
buffsize = 4096
	
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #option for force socket reusing
    s.bind((host,port))
    s.listen(1)

except socket.error as msg:
    print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror))
    sys.exit()

while True:
    client, address = s.accept()
    data = client.recv(buffsize)
    while data != b"":
        client.send(data)
        data = client.recv(buffsize)
