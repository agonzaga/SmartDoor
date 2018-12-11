import socket
import select

UDP_IP = "127.0.0.1"
IN_PORT = 5005
timeout = 3


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, IN_PORT))

print("Running UDP server on {}:{}".format(UDP_IP, IN_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    if data:
        print("Recieved file:" + data.decode())
        file_name = data.strip()

    f = open(file_name, 'wb')

    while True:
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            data, addr = sock.recvfrom(1024)
            f.write(data)
        else:
            print("Downloaded " + file_name.decode())
            f.close()
            break