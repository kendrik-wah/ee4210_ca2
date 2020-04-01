from socket import *

protocol = 0
timeout = 30
hostname = "127.0.0.1"
port = 8000
message = "Hey, server!".encode()

def create_client():
	sock = socket()
	sock.settimeout(timeout)
	return sock

def connect(sock, host, port):

	sock.connect((host, port))
	try:
		data = sock.recv(1024)
	except socket.error:
		print('[client]: socket receive error')
		sys.exit(1)

	print(data)

	return data

def send_message(sock, message):
	sock.sendall(message)
	data = sock.recv(1024)
	sock.close()
	return data

test = create_client()
data = connect(test, hostname, port)
data = send_message(test, message)

print(data)

