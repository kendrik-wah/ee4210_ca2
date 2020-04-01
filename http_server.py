import socket
import json
import datetime
import sys
import os

with open('locn.json', 'r') as j:
	parsed_json = json.loads(j.read())

HOSTNAME = parsed_json["hostname"]
PORT = parsed_json["port"]
PROTOCOL = parsed_json["protocol"]
TIMEOUT = parsed_json["timeout"]
MAX_SIZE = parsed_json["max_size"]
QUEUE_SIZE = parsed_json["queue_size"]
PERSISTENT = parsed_json["persistent"]
NON_PERSISTENT = parsed_json["non_persistent"]

def setup_server(hostname, port):

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, PROTOCOL) # TCP connection
	except socket.error:
		print("[server]: socket setup has failed.")
		sys.exit(1)

	sock.settimeout(TIMEOUT)
	sock.bind((hostname, port))

	try:
		sock.listen(QUEUE_SIZE)
	except socket.error:
		print("[server]: setting up socket queue failed.")
		sys.exit(1)

	return sock



def create_conn(sock):

	try:
		conn, acc = sock.accept()
	except socket.timeout:
		print("[server]: no connections established after {} seconds. terminating connection.".format(TIMEOUT))
		sys.exit(1)

	if (conn.fileno() < 0):
		print("[server]: no connections established. terminating server.")
		sys.exit(1)

	test = receive_data(conn)

	if test != 'con'.encode():
		print("[server]: acknowledge from client failed. shutting down server.")
		sys.exit(1)

	send_data(conn, 'con'.encode())
	

	return conn


def send_data(sock, data):

	try:
		sock.sendall(data)
	except socket.error:
		print("[server]: error sending data.")
		sys.exit(1)



def receive_data(sock):

	try:
		data = sock.recv(MAX_SIZE)
	except socket.error:
		print("[server]: error receiving data.")
		sys.exit(1)
	return data



def send_file(sock, data):


	'''
	1) Open the file as given be data.
	2) while loop is running:
		a) line <- 1024 bytes worth of data from the file. 
		b) if line is empty:
			- send 'fin' to indicate end of file.
			- break loop and end.
		c) else, send the data.
		d) receive ack from client.
		e) if ack != 'ack', break the loop. 
	3) close the file.
	'''

	file = open(data[1][1:], 'rb')
	
	while True:

		line = file.read(MAX_SIZE)
		if not line:
			print('[server]: reached end of file, sending fin to client.')
			send_data(sock, 'fin'.encode())
			break

		send_data(sock, line)
		ack = receive_data(sock)
		if not ack == 'ack'.encode():
			print('[server]: ack not received, end file sending.')
			break

	file.close()



if __name__ == "__main__":

	sock = setup_server(HOSTNAME, PORT)
	conn = create_conn(sock)

	while True:
		print('[server]: receiving request from client now, field descriptor at {}.'.format(conn.fileno()))
		data = receive_data(conn)

		if data:
			print('\n[server]: request obtained - {}'.format(data.decode()))
			data = data.split()
			filename = data[1][1:]
			conn_type = data[6]

			if conn_type == NON_PERSISTENT.encode():

				send_file(conn, data)
				print("[server]: {} sent. closing file and shutting down connection.".format(filename.decode()))
				conn.close()
				print("[server]: socket has been closed. field descriptor is {}.\n".format(conn.fileno()))
				conn = None
				conn = create_conn(sock)

			elif (conn_type == PERSISTENT.encode()):
				send_file(conn, data)

		else:
			print('[server]: no more requests from client.')
			break

	if conn.fileno() > 0:
		print("[server]: all files requested, now closing socket.")
		sock.close()
		print("[server]: socket has been closed. field descriptor is {}.\n".format(sock.fileno()))
		sock = None