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
FILE_A = parsed_json["file_a"]
FILE_B = parsed_json["file_b"]
FILE_C = parsed_json["file_c"]

files = [FILE_A, FILE_B, FILE_C]

def connect(hostname, port):
	try:
		sock.connect((hostname,port))
	except:
		raise Exception("client connection failed!")

def send_message(msg):
	try:
		sock.sendall(msg.encode())
	except:
		raise Exception("send message failed!")

	data = sock.recv(16)
	return data

if __name__ == "__main__":
	sock = socket.socket()
	sock.settimeout(TIMEOUT)
	connect(HOSTNAME, PORT)

	for file in files:
		data = send_message(file)
