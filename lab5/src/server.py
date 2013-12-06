#!/usr/bin/env python3
import socket, signal, sys, os, time

buffsize = 128
path = ""

def ensure_dir(path):
    d = os.path.dirname(path)
    if not os.path.exists(d):
        os.makedirs(d, 0o777)

def sigterm(signo, sigobj):
    print("SIGTERM: {0} Exitting...".format(signo))
    sys.exit()

def _recieveFile(server, addr, path):
    global buffsize

    ensure_dir(path)    #Create directory
    global sendLen
    recvLen = 0
    size, addr = server.recvfrom(10)
    sendLen = int(size.decode("utf-8"));
    time.sleep(0.001)
    print(sendLen)

    recieveFile = open(path, 'wb')

    data, addr = server.recvfrom(buffsize)
    while (data != b""):
        print(data)
        time.sleep(0.001)
        recieveFile.write(data)
        recvLen += len(data)
        print(recvLen, "/", sendLen)
        if(recvLen == sendLen):
            break
        server.settimeout(2)
        data, addr = server.recvfrom(buffsize)

    recieveFile.close()

    print(sendLen, os.stat(path).st_size)
    if sendLen != os.stat(path).st_size:
        print("Error when receiving file data. ", os.stat(path).st_size, " from ", sendLen)

signal.signal(signal.SIGTERM, sigterm)
signal.signal(signal.SIGINT, sigterm)

if len(sys.argv) == 3:
    host = sys.argv[1]
    port = int(sys.argv[2])
elif len(sys.argv) == 2:
    host = "localhost"
    port = int(sys.argv[1])
else:
    print("Usage: server.py [hostname] <port>")
    sys.exit()

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #option for force socket reusing
    server.bind((host,port))

except socket.error as msg:
    print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror))
    sys.exit()

while True:
    data, addr = server.recvfrom(buffsize)
    time.sleep(0.001)
    print(data)
    _recieveFile(server, addr, "./recieved/" + str(data, "UTF-8"))

server.close()
