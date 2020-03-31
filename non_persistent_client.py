import socket
import json
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
FILE_A = parsed_json["file_a_non_persistent"]
FILE_B = parsed_json["file_b_non_persistent"]
FILE_C = parsed_json["file_c_non_persistent"]

files = [FILE_A, FILE_B, FILE_C]

def make_socket():
	sock = socket.socket()
	sock.settimeout(TIMEOUT)
	print("[client]: socket created. timeout is set at {} seconds.".format(TIMEOUT))
	return sock



def connect(hostname, port):

	try:
		sock.connect((hostname,port))
	except socket.error:
		print("[client]: connection has been refused. check the server.")
		sys.exit(1)

	print("[client]: socket is requesting from a server at {} and {}.".format(hostname, port))



def send_data(sock, msg):

	try:
		sock.sendall(msg.encode())
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



def retrieve_file(sock, raw_filename, extension):

	filename='retrieve_non_persistent_' + raw_filename + extension
	print("[client]: will write to {}.".format(filename))
	file = open(filename, 'wb+')
	print("[client]: {} created.".format(filename))

	datum = True
	while datum:
		datum = receive_data(sock)
		if datum == 'fin'.encode() or not datum:
			print('[client]: empty line received. ending file retrieval from server.')
			break

		file.write(datum)
		send_data(sock, 'ack')
	file.close()
	print("[client]: finished writing to {}. file closed.".format(filename))



def send_message(sock, msg, filename):

	raw_filename, file_ext = os.path.splitext(filename)

	send_data(sock, msg)
	print("[client]: request has been sent.")
	retrieve_file(sock, raw_filename, file_ext)
	print("[client]: {} has been received, now closing client socket.".format(filename))



if __name__ == "__main__":
	
	for file in files:

		filename = file.split()[1][1:]
		print("[client]: requesting for {}.".format(filename))

		sock = make_socket()
		connect(HOSTNAME, PORT)
		send_message(sock, file, filename)
		sock.close()
		print("[client]: socket has been closed. field descriptor is {}.\n".format(sock.fileno()))
		sock = None