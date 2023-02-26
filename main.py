from udp import udp_init
from mqtt import mqtt_init, make_message
from config import CARE_TOPIC


if __name__ == "__main__":
    sock = udp_init()
    client = mqtt_init()

    client.loop_start()

    print("Waiting to receive data...")
    while True:
        data, addr = sock.recvfrom(512)
        print("received:", data, " from", addr)
        msg = make_message(data)
        client.publish(CARE_TOPIC, msg, 1)



        
