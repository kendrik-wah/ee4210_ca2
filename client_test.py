from socket import *

protocol = 0
timeout = 5
hostname = gethostname()
port = 65430
message = "Welcome user".encode()

def create_client():
	sock = socket()
	return sock

def connect(sock, host, port):
	sock.connect((host, port))
	return sock

def send_message(sock, message):
	sock.sendall(message)
	data = sock.recv(1024)
	sock.close()
	return data

test = create_client()
test = connect(test, hostname, port)

data = send_message(test, message)

print(data)

