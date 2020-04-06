import socket
import json
import datetime
import sys
import os

protocol = 0
timeout = 30
hostname = "127.0.0.1"
port = 8000
message = "test".encode()
MAX_SIZE = 1024

def create_client():
	sock = socket.socket()
	sock.settimeout(timeout)
	return sock



def connect(sock, hostname, port):

	t1 = datetime.datetime.now()

	try:
		sock.connect((hostname,port))
	except socket.error:
		print("[client]: connection has been refused. check the server.")
		sys.exit(1)

	send_data(sock, 'con'.encode())
	data = receive_data(sock)

	if data != 'con'.encode():
		print('[client]: connection to server not acknowledged. shutting down client.')
		sys.exit(1)

	t2 = datetime.datetime.now()

	send_data(sock, 'ack'.encode())

	return (t2-t1).total_seconds()



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



if __name__ == "__main__":
	sock = create_client()
	time_diff = connect(sock, hostname, port)

	t3 = datetime.datetime.now()
	

	send_data(sock, 'ack'.encode())
	new_data = receive_data(sock)	

	t4 = datetime.datetime.now()

	print("[client]: connect establishment time = {}".format(time_diff))
	print("[client]: ack sending time = {}".format((t4-t3).total_seconds()))