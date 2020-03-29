import http.server
import socket
import json
import sys

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

def handle_persistent(conn, data, filename):

	while data:
	send_file(conn, data)
	print("[server]: {} sent. closing file.".format(filename.decode()))
	data = receive_data(conn)

	conn.close()
	conn = None



def handle_non_persistent(conn, data, filename):

	send_file(conn, data)
	print("[server]: {} sent. closing file and shutting down connection.".format(filename.decode()))
	conn.close()
	conn = None



def setup_server(hostname, port):

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, PROTOCOL) # TCP connection
	except socket.error:
		print("[server]: socket setup has failed.")
		sys.exit(1)

	sock.settimeout(TIMEOUT)
	print("[server]: socket created. timeout is set at {} seconds.".format(TIMEOUT))
	sock.bind((hostname, port))
	print("[server]: socket created in server at {} and {}.".format(HOSTNAME, PORT))

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

	print("[server]: client found at {}".format(acc))
	return conn


def send_data(sock, data):

	try:
		sock.send(data)
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

	file = open(data[1][1:], 'rb')
	
	while True:
		line = file.read(MAX_SIZE)
		if not line:
			break

		send_data(sock, line)

	file.close()



if __name__ == "__main__":

	sock = setup_server(HOSTNAME, PORT)
	conn = create_conn(sock)

	while True:
		data = receive_data(conn)
		print('\n')
		data = data.split()
		filename = data[1][1:]
		conn_type = data[6]

		if conn_type == NON_PERSISTENT.encode():
			handle_non_persistent(conn, data, filename)
			conn = create_conn(sock)

		elif (conn_type == PERSISTENT.encode()):
			handle_persistent(conn, data, filename)
			break