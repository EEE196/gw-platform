import socket
from publish import init_mqtt
from config import UDP_IP, UDP_PORT

def udp_init():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind((UDP_IP, UDP_PORT))

    return sock

