import socket
import select
import os


UDP_IP = "155.41.64.232"
IN_PORT = 5005
timeout = 3


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, IN_PORT))

print("Running UDP server on {}:{}".format(UDP_IP, IN_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    if data:
        file_name = data.strip()

    try:
    	os.system("mkdir training_sets/" + file_name.decode()[:-5])
    except:
    	pass

    f = open("training_sets/" + file_name.decode()[:-5] + '/' + file_name.decode(), 'wb')

    while True:
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            data, addr = sock.recvfrom(1024)
            f.write(data)
        else:
            print("Downloaded " + file_name.decode())
            f.close()
            break

