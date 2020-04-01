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
FILE_A = parsed_json["file_a_non_persistent"]
FILE_B = parsed_json["file_b_non_persistent"]
FILE_C = parsed_json["file_c_non_persistent"]

files = [FILE_A, FILE_B, FILE_C]

def make_socket():

	try:
		sock = socket.socket()
		sock.settimeout(TIMEOUT)
	except socket.error:
		print('[client]: socket creation has failed. closing the client')
		sys.exit(1)
		
	return sock



def connect(hostname, port):

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
	return (t2-t1)



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



def retrieve_file(sock, raw_filename, extension):

	filename='retrieve_non_persistent_' + raw_filename + extension
	file = open(filename, 'wb+')
	count = 0

	datum = True
	while datum:

		datum = receive_data(sock)
		if datum == 'fin'.encode() or not datum:
			break

		file.write(datum)
		count += 1
		send_data(sock, 'ack'.encode())

	file.close()
	return count



if __name__ == "__main__":

	total_time = 0
	number_of_packets = 0
	
	for file in files:

		filename = file.split()[1][1:]
		raw_filename, file_ext = os.path.splitext(filename)

		sock = make_socket()
		t0 = connect(HOSTNAME, PORT)

		t1 = datetime.datetime.now()
		# print('[client]: current time is {}.'.format(t1)) # Find the time prior to making the socket.

		send_data(sock, file.encode())
		pkt_rec = retrieve_file(sock, raw_filename, file_ext)

		sock.close() # Close socket. End connection.
		sock = None

		t2 = datetime.datetime.now()
		# print('[client]: current time is {}.'.format(t2)) # Find the time after making the socket.

		time_diff = (t2-t1+t0).total_seconds()
		print('[client]: time difference is {} seconds.'.format(time_diff)) # Calculated time difference.
		total_time += time_diff

		print('[client]: number of packets received = {}\n'.format(pkt_rec)) # Find the number of packets received.
		number_of_packets += pkt_rec

	print('[client]: transaction time = {} seconds.'.format(total_time))
	print('[client]: number_of_packets = {}'.format(number_of_packets))
