from udp import udp_init

if __name__ == "__main__":
    sock = udp_init()
    key = '00000000000000000000000000000000'
    dev_addr = 'DEADBEEF'

    print("Waiting to receive data...")
    while True:
        data, addr = sock.recvfrom(512)

        data = data[12:].decode('utf8')
        try:
            data = json.loads(data)
            data = data['rxpk'][0]['data']
            print(data)
        except:
            pass       
