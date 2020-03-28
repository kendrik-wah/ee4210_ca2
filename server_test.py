from socket import *

protocol = 0
timeout = 30
hostname = gethostname()
port = 65430

def make_socket(protocol, timeout):

	sock = 0

	try:
		sock = socket(AF_INET, SOCK_STREAM, protocol)
		sock.settimeout(timeout)
	except:
		raise Exception("socket error has occurred")

	return sock

def bind_socket(sock, hostname, port):

	try:
		sock.bind((hostname, port))
	except:
		raise Exception("error in binding hostname and port")

	return sock

def echo_socket(socket):

	try:
		test = socket.listen()
	except (test < 0):
		raise Exception("listen error")

	conn, addr = socket.accept()
	print('Got connection from ', addr[0], '(', addr[1], ')')
	print('Thank you for connecting')

	with conn:
		while True:
			data = conn.recv(1024)
			if not data:
				break

			print(data)
			conn.sendall(data)

		conn.close()

test = make_socket(protocol, timeout)
print(test)

test = bind_socket(test, hostname, port)
print(test)

echo_socket(test)