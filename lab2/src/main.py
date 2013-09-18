import socket, sys

host = sys.argv[1]
port = int(sys.argv[2])

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(1)

except socket.error as msg:
    print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror))
    sys.exit()

while True:
    client, address = s.accept()
    data = ''
    while data != 'exit':
        data = client.recv(1024)
        if not data: 
            break
        elif data == 'bye':
            client.close();
        elif data == 'exit':
            client.close();
            sys.exit()
        else:
            client.send("Echo: " + data)

