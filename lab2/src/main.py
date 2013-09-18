import socket, sys

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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #option for correct socket closing
    s.bind((host,port))
    s.listen(1)

except socket.error as msg:
    print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror))
    sys.exit()

try:
    client, address = s.accept()
    while True:
        data = client.recv(4096)
        if not data: 
            break
        else:
            client.send(data)
except KeyboardInterrupt:
    s.close()
    sys.exit()
