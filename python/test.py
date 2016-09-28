import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 8082))

while True:
	resp = s.recv(1024)
	if resp == "": 
		break

s.close()

