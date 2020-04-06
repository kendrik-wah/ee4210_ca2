import socket
import json
import datetime
import sys
import os

protocol = 0
timeout = 10
hostname = "127.0.0.1"
port = 8000
ret_msg = "test".encode()
MAX_SIZE = 1024

def make_socket(protocol, timeout):

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) # TCP connection
	except socket.error:
		print('[client]: socket creation has failed. closing the client')
		sys.exit(1)

	sock.bind((hostname, port))
	sock.settimeout(10)
		
	return sock



def create_conn(sock):

	try:
		conn, acc = sock.accept()
	except socket.timeout:
		print("[server]: no connections established after {} seconds. terminating connection.".format(10))
		sys.exit(1)

	if (conn.fileno() < 0):
		print("[server]: no connections established. terminating server.")
		sys.exit(1)

	test = receive_data(conn)

	if test != 'con'.encode():
		print("[server]: acknowledge from client failed. shutting down server.")
		sys.exit(1)

	send_data(conn, 'con'.encode())

	test = receive_data(conn)

	if test != 'ack'.encode():
		print("[server]: acknowledge from client failed. shutting down server.")
		sys.exit(1)

	return conn



def send_data(sock, msg):

	try:
		sock.sendall(msg)
	except socket.error:
		print("[client]: send message failed.\n")
		sys.exit(1)



def receive_data(sock):

	try:
		data = sock.recv(MAX_SIZE)
	except socket.error:
		print("[client]: error in receiving data.")
		sys.exit(1)

	return data



def listen_client(sock):

	try:
		test = sock.listen(5)
	except socket.error:
		print("[server]: listen error")
		sys.exit(1)



if __name__ == '__main__':

	sock = make_socket(protocol, timeout)
	listen_client(sock)
	conn = create_conn(sock)

	new_data = receive_data(conn)
	send_data(conn, 'ack'.encode())
	