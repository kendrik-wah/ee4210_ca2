==================
= Prerequisites: =
==================
==============================================================================
To run the code, ensure that your device has the following prerequisites met:
1) Python 3.6.5
2) Installation of the following libraries:
	a) socket
	b) json
	c) datetime
	d) sys
	e) os
==============================================================================
=======================
= Contents of folder: =
=======================
==============================================================================
This folder contains 5 Python scripts and 1 JSON file.

For testing purposes:
1) client_test.py
2) server_test.py

Notice that client_test.py and server_test.py does not rely on stored variables in locn.json.

For the actual assignment:
1) http_server.py
2) persistent_client.py
3) non_persistent_client.py

The constants are stored in locn.json.
Inside locn.json contains the following key-value pairs:

{
	"hostname": "127.0.0.1",
	"port": 8000,
	"protocol": 0,
	"timeout": 10,
	"max_size": 1024,
	"queue_size": 5,
	"file_a_persistent": "GET /a.jpg HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nConnection: keep-alive\r\n\n",
	"file_b_persistent": "GET /b.mp3 HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nConnection: keep-alive\r\n\n",
	"file_c_persistent": "GET /c.txt HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nConnection: keep-alive\r\n\n",
	"file_a_non_persistent": "GET /a.jpg HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nConnection: close\r\n\n",
	"file_b_non_persistent": "GET /b.mp3 HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nConnection: close\r\n\n",
	"file_c_non_persistent": "GET /c.txt HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nConnection: close\r\n\n",
	"file_a_expected": 31,
	"file_b_expected": 4684,
	"file_c_expected": 1,
	"persistent": "keep-alive",
	"non_persistent": "close"
}
Feel free to copy this to reinitialize any changes you have made but have forgotten.
==============================================================================
===============
= How to use: =
===============
==============================================================================
1) To use the client and server, open the terminal and change directory to the folder where the script and client are kept.
   One script and one client uses one terminal each.
2) To run the server, run 'python http_server.py'.
3a) To run the non-persistent client, run 'python non_persistent_client.py'.
3b) To run the persistent client, run 'python persistent_client.py'.

Step 3 has to be run within 10 seconds. This is because the timeout is at 10.
To change the timeout, open locn.json and change the value as required.
==============================================================================