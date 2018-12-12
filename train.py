import face_recog
import os
import socket
import time
import sys
import paramiko

IP = "168.122.3.107"
TCP_PORT = 7777

def main():
	time.sleep(5)
	os.system("python face_recog.py -t")
	sendyml()



def sendyml():
	buf = 1024
	file_name = 'model.yaml'

	sock = socket.socket()
	sock.connect((IP, TCP_PORT))
	f = open(file_name, "rb")
	data = f.read(buf)
	while(data):
		sock.send(data)
		data = f.read(buf)

	sock.close()
	f.close()


if __name__ == '__main__':
	main()