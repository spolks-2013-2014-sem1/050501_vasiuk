#!/usr/bin/env python3
import socket, signal, sys, os, time

buffsize = 128

def sigterm(signo, sigobj):
    print("SIGTERM: {0} Exitting...".format(signo))
    sys.exit()

def _sendFile(client, path):
    global buffsize
    if not os.path.isfile(path):
        print("File " + path + " is not exist")
        return

    client.send(bytes(str(os.stat(path).st_size), "utf-8"))
    time.sleep(0.001)

    count = int((os.stat(path).st_size)/buffsize/10)        #send message every 10% 
    if count == 0:
        count = 4
    
    sendFile = open(path, 'rb')
    sentData = 0
    sendOob = 0
    data = sendFile.read(buffsize)
    while data != b"":
        client.send(data)
        sentData += len(data)
        data = sendFile.read(buffsize)
        time.sleep(0.001)
        sendOob += 1
        if sendOob % count == 0:
            sendOob = 0
            client.send(b"!Q", socket.MSG_OOB)
            time.sleep(0.001)

signal.signal(signal.SIGTERM, sigterm)
signal.signal(signal.SIGINT, sigterm)

if len(sys.argv) == 3:
    host = sys.argv[1]
    port = int(sys.argv[2])
elif len(sys.argv) == 2:
    host = "localhost"
    port = int(sys.argv[1])
else:
    print("Usage: server..py [hostname] <port>")
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
    _sendFile(client, data.decode("utf-8"))
    client.close()
