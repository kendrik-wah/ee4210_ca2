import socket
import json

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
	sock = socket.socket()
	sock.settimeout(TIMEOUT)
	sock.setblocking(0)
	return sock


def connect(hostname, port):
	try:
		sock.connect((hostname,port))
	except socket.error:
		print("[client]: connection has been refused. check the server.")
		sys.exit(1)



def send_data(sock, msg):

	try:
		sock.sendall(msg)
	except socket.error:
		print("[client]: send message failed.")
		sys.exit(1)


def receive_data(sock):

	try:
		data = sock.recv(MAX_SIZE) # This line is the problem.
	except socket.error:
		print("[client]: error in receiving data.")
		sys.exit(1)

	return data



def retrieve_file(sock):

	data = []
	while True:
		datum = receive_data(sock)
		if not datum or datum == 'EOF':
			break
		data.append(datum)

	return data



def request_client(sock):

	data = {}

	for file in files:
		filename = file.split()[1][1:]

		print("[client]: requesting for {}".format(filename))
		send_data(sock, file.encode())
		data[file] = retrieve_file(sock)
		print("[client]: received {}\n".format(filename))

	print(data)


if __name__ == "__main__":

	sock = socket.socket()
	print("[client]: socket created. timeout is set at {} seconds.".format(TIMEOUT))
	connect(HOSTNAME, PORT)
	print("[client]: socket connected to and will request files from a server at {} and {}.\n".format(HOSTNAME, PORT))
	request_client(sock)
	print("[client]: all files retrieved. now closing socket.")
	sock.close()
