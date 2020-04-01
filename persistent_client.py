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
FILE_A = parsed_json["file_a_persistent"]
FILE_B = parsed_json["file_b_persistent"]
FILE_C = parsed_json["file_c_persistent"]

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
	return (t2-t1).total_seconds()



def send_data(sock, msg):

	try:
		sock.sendall(msg)
	except socket.error:
		print("[client]: send message failed.")
		sys.exit(1)



def receive_data(sock):

	try:
		data = sock.recv(MAX_SIZE)
	except socket.error:
		print("[client]: error in receiving data.")
		sys.exit(1)

	return data



def retrieve_file(sock, raw_filename, extension):

	'''
	This function call only works for a SINGLE file.

	1) Create a file to write to.
	2) while loop is running
		a) receive data from the socket.
			- if data == 'fin' or data is an empty string, the last bits of data have been transmitted.
			  in this case, break the loop since there is no more data to be received.
		b) write data to file.
		c) record packet received. do not count 'fin' as a received packet.
		d) send an acknowledge to the server, telling the server to continue sending the packet.
	3) close the file to write to. good practice, might accidentally write mp3 files into txt and etc etc etc.
	4) return the number of packets recorded for the file retrieved.
	'''

	filename='retrieve_persistent_' + raw_filename + extension
	file = open(filename, 'wb+')

	datum = True
	count = 0

	while datum:

		datum = receive_data(sock)
		if datum == 'fin'.encode() or not datum:
			# print('[client]: end of file acknowledged. ending file retrieval from server.')
			break

		file.write(datum)
		count += 1
		send_data(sock, 'ack'.encode())

	file.close()
	return count



if __name__ == "__main__":

	number_of_packets = 0
	sock = make_socket()
	t0 = connect(HOSTNAME, PORT)
	total_time = t0

	for file in files:

		filename = file.split()[1][1:]
		raw_filename, file_ext = os.path.splitext(filename)

		t1 = datetime.datetime.now()
		# print('[client]: current time is {}.'.format(t1)) # Record time before sending request.

		send_data(sock, file.encode()) # Send file request to server.
		pkt_rec = retrieve_file(sock, raw_filename, file_ext) # Retrieve file, record number of packets received from server.

		t2 = datetime.datetime.now()
		# print('[client]: current time is {}.'.format(t2)) # Record time after transaction.

		time_diff = (t2-t1).total_seconds()
		print('[client]: time difference is {} seconds.'.format(time_diff)) # Calculated time difference.
		total_time += time_diff

		print('[client]: number of packets received = {}\n'.format(pkt_rec)) # Find the number of packets received.
		number_of_packets += pkt_rec

	print('[client]: transaction time = {} seconds.'.format(total_time))
	print('[client]: number_of_packets = {}'.format(number_of_packets))

	sock.close()
	sock = None