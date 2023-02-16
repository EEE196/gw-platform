import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

UDP_IP = socket.gethostname()
UDP_PORT = 2100

sock.bind((UDP_IP, UDP_PORT))

while True:
    print("Waiting for client...")
    data, addr = sock.recvfrom(256)
    print("Received Messages:", data, " from", addr)


