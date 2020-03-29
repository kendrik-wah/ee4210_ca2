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
FILE_A = parsed_json["file_a_non_persistent"]
FILE_B = parsed_json["file_b_non_persistent"]
FILE_C = parsed_json["file_c_non_persistent"]

files = [FILE_A, FILE_B, FILE_C]

def make_socket():
	sock = socket.socket()
	sock.settimeout(TIMEOUT)
	return sock



def connect(hostname, port):
	try:
		sock.connect((hostname,port))
	except ConnectionRefusedError:
		print("[client]: connection has been refused. check the server.")
		raise ConnectionRefusedError
	except:
		print("[client]: client connection failed.")
		raise Exception



def send_message(msg, filename):
	try:
		print(msg)
		sock.sendall(msg.encode())
	except:
		print("[client]: send message failed.\n")
		raise Exception

	print("[client]: send message completed.")
	datum = True
	data = []
	
	while datum:
		datum = sock.recv(MAX_SIZE)
		if not datum:
			break
		else:
			data.append(datum)

	print('[client]: request completed.')
	print(data)

	print("[client]: {} has been received, now closing client socket.\n".format(filename))
	sock.close()



if __name__ == "__main__":
	
	for file in files:

		filename = file.split()[1][1:]

		sock = socket.socket()
		print("[client]: socket created. timeout is set at {} seconds.".format(TIMEOUT))
		connect(HOSTNAME, PORT)
		print("[client]: socket connected to and will request files from a server at {} and {}.".format(HOSTNAME, PORT))
		send_message(file, filename)
