import http.server
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
PERSISTENT = parsed_json["persistent"]
NON_PERSISTENT = parsed_json["non_persistent"]

'''
[b'GET', b'/a.jpg', b'HTTP/1.1', b'Host:', b'127.0.0.1:8080', b'Connection:', b'keep-alive']
'''

def handle_file(filename, connection, conn_type):
	if conn_type == PERSISTENT:
		handle_persistent(filename, connection)	
	elif conn_type == NON_PERSISTENT:
		handle_non_persistent(filename, connection)

def handle_request(connection):

	try:
		data = connection.recv(MAX_SIZE).split()
	except:
		raise Exception("data extraction failed!")

	filename = data[1][1:]
	conn_type = data[6]

	handle_file(filename, connection, conn_type)



	print(data)
	if not data:
		return False
	return True

def setupServer(hostname, port):

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, PROTOCOL) # TCP connection
	except:
		raise Exception("socket setup has failed!")

	print(sock)
	sock.settimeout(TIMEOUT)
	sock.bind((hostname, port))
	return sock

def serveForever(sock):

	try:
		sock.listen(QUEUE_SIZE)
	except:
		raise Exception("socket listen has failed!")

	conn, acc = sock.accept()
	print(sock)
	data = True
	while data:
		data = handle_request(conn)
		if not data:
			break

	conn.close()

if __name__ == "__main__":
	sock = setupServer(HOSTNAME, PORT)
	serveForever(sock)