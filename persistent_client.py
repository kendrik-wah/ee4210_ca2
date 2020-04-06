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
EXPECTED_A = parsed_json["file_a_expected"]
EXPECTED_B = parsed_json["file_b_expected"]
EXPECTED_C = parsed_json["file_c_expected"]

files = [FILE_A, FILE_B, FILE_C]
file_sizes = {'a': EXPECTED_A, 'b': EXPECTED_B, 'c': EXPECTED_C}

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

	send_data(sock, 'SYN'.encode())
	data = receive_data(sock)

	if data != 'SYN_ACK'.encode():
		print('[client]: connection to server not acknowledged. shutting down client.')
		sys.exit(1)

	t2 = datetime.datetime.now()

	send_data(sock, 'ACK'.encode())

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



def check_pkts(raw_filename, pkt_rec):

	if (file_sizes[raw_filename] != pkt_rec):
		print('[client]: file transmission error. some packets were lost.')
		sys.exit(1)



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
		if datum == 'FIN'.encode() or not datum:
			# print('[client]: end of file acknowledged. ending file retrieval from server.')
			break

		file.write(datum)
		count += 1
		send_data(sock, 'ACK'.encode())

	file.close()
	return count



if __name__ == "__main__":

	number_of_packets = 0
	sock = make_socket()
	total_time = connect(HOSTNAME, PORT) # account for connecting time.

	print("[client]: t0 = {} seconds.\n".format(total_time))

	for file in files:

		filename = file.split()[1][1:]
		raw_filename, file_ext = os.path.splitext(filename)

		t1 = datetime.datetime.now() # Record time before sending request.

		send_data(sock, file.encode()) # Send file request to server.
		http_response = receive_data(sock)

		t2 = datetime.datetime.now() # Record time after receiving response.

		if (http_response == 'Response 200'.encode()):
			pkt_rec = retrieve_file(sock, raw_filename, file_ext)

		check_pkts(raw_filename, pkt_rec) # ensure no file transmission error

		t3 = datetime.datetime.now() # Record time after transaction.

		time_diff = (t3-t1).total_seconds()
		print('[client]: response time is {} seconds.'.format((t2-t1).total_seconds()))
		print('[client]: time difference is {} seconds.'.format((t3-t2).total_seconds())) # Calculated time difference.
		total_time += time_diff

		print('[client]: number of packets received = {}\n'.format(pkt_rec)) # Find the number of packets received.
		number_of_packets += pkt_rec

	print('[client]: transaction time = {} seconds.'.format(total_time))
	print('[client]: number_of_packets = {}'.format(number_of_packets))

	send_data(sock, 'FIN'.encode())
	fin_data = receive_data(sock)
	if (fin_data == 'FIN_ACK'.encode()):
		send_data(sock, 'ACK'.encode())

	sock.close()
	sock = None