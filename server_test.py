from socket import *
import time
import sys

protocol = 0
timeout = 30
hostname = "127.0.0.1"
port = 8000
ret_msg = "Hello, client!".encode()

def make_socket(protocol, timeout):

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
	except socket.error:
		print("[server]: listen error")
		sys.exit(1)

	try:
		conn, addr = socket.accept()
	except socket.error:
		print("[server]: accept error")
		sys.exit(1)

	print('Got connection from ', addr[0], '(', addr[1], ')')
	try:
		conn.sendall('Thank you for connecting'.encode())
	except socket.error:
		print("[server]: sending error")
		sys.exit(1)

	with conn:
		data = True
		while data:
			data = conn.recv(1024)
			if not data:
				break
			else: 
				print("Acquired data: ", data.decode())
				conn.sendall(ret_msg)
				print("Sent message: ", ret_msg.decode())

		print("Disconnected.")
		conn.close()

if __name__ == '__main__':

	test = make_socket(protocol, timeout)
	test = bind_socket(test, hostname, port)
	echo_socket(test)