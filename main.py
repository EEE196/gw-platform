from udp import udp_init


if __name__ == "__main__":
    sock = udp_init()


    print("Waiting to receive data...")
    while True:
        data, addr = sock.recvfrom(256)
        print("received:", data, " from", addr)



        
