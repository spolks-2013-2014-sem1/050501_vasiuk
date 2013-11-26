#!/usr/bin/env python3
import socket, signal, sys, os

buffsize = 128

def ensure_dir(path):
    d = os.path.dirname(path)
    if not os.path.exists(d):
        os.makedirs(d, 0o777)

def sigterm(signo, sigobj):
    print("SIGTERM: {0} Exitting...".format(signo))
    sys.exit()

def _recieveFile(server, path):
    global buffsize

    ensure_dir(path)    #Create directory
    sendlen = server.recv(4).decode("utf-8");

    recieveFile = open(path, 'wb')

    recvLen = 0
    data = "start"
    while data != b"":
        try:
            data = server.recv(buffsize, socket.MSG_OOB)
        except socket.error:
            data = None
        if data:
            print("Recieved ", recvLen, "/", sendlen)
        else:
            data = server.recv(buffsize)
            recieveFile.write(data)
            recvLen += len(data)

    recieveFile.close()

    if sendlen != recvLen:
        print("Error when receiving file data.")

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
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host,port))

except socket.error as msg:
    print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror))
    sys.exit()

server.send(bytes(path, "utf-8"))

_recieveFile(server, "./recieved/" + os.path.basename(path))
server.close()