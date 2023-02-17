from udp import udp_init
from mqtt import mqtt_init, make_message


if __name__ == "__main__":
    sock = udp_init()
    client = mqtt_init()

    client.loop_start()

    print("Waiting to receive data...")
    while True:
        data, addr = sock.recvfrom(256)
        print("received:", data, " from", addr)
        msg = make_message(data)
        client.publish('CARE6/UAV', msg, 1)



        
