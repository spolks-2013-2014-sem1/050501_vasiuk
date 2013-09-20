#!/usr/bin/env python

import socket, signal, sys, threading

buffsize = 4096
threads = []

class ClientThread(threading.Thread):

    def __init__(self, ip, port, socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket

    def run(self):    
        data = self.socket.recv(2048)

        while len(data):
            self.socket.send(data)
            data = self.socket.recv(2048)
        self.socket.close()

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

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #option for force socket reusing
    server.bind((host,port))

except socket.error as msg:
    print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror))
    sys.exit()

while True:
    server.listen(5)
    (client, (ip, port)) = server.accept()
    newthread = ClientThread(ip, port, client)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()