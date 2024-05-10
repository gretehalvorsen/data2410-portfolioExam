def gbn_client(args):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(5)

    syn_packet = create_packet(0, 0, 1, b'')
    send_packet(client_socket, syn_packet, (args.ip, args.port))

    base = 1
    next_seq = 1
    window_size = args.window_size
    pkt_buffer = queue.Queue()
    eof = False

    with open(args.file, "rb") as f: 
        while not eof or not pkt_buffer.empty():
            while next_seq < base + window_size and not eof:
                data = f.read(994)
                if not data:
                    eof = True
                else:
                    data_packet = create_packet(next_seq, 0, 0, data)
                    send_packet(client_socket, data_packet, (args.ip, args.port))
                    pkt_buffer.put((next_seq, data_packet))
                    next_seq += 1

            if pkt_buffer.empty():
                break
    
            try:
                _, _, seq, ack, _ = recv_packet(client_socket)
                print(f"Received ACK for sequence number: {ack}")  # Debug print
                while base <= ack:
                    _, _ = pkt_buffer.get()
                    base += 1

            except socket.timeout:
                print("Timeout occurred")  # Debug print
                for i in range(pkt_buffer.qsize()):
                    seq, data_packet = pkt_buffer.queue[i]
                    send_packet(client_socket, data_packet, (args.ip, args.port))

        # Send EOF packet after all data has been sent and ACKs received
    eof_packet = create_packet(next_seq, 0, 1, b'')
    send_packet(client_socket, eof_packet, (args.ip, args.port))      

def gbn_server(args):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((args.ip, args.port))

    if args.file is None:
        recvd_file = open("image.jpg", "wb")
    else:
        recvd_file = open(args.file, "wb")

    expected_seq = 1

    while True:
        msg, client_addr, seq, ack, flags = recv_packet(server_socket)
        print(f"Received packet with sequence number: {seq}")  # Debug print

        # If the EOF packet is received
        if flags == 1 and seq == expected_seq:
            recvd_file.close()
            break

        elif seq == expected_seq:
            recvd_file.write(msg[6:])
            #print(f"Wrote data to file: {msg[6:]}")  # Debug print
            send_packet(server_socket, create_packet(0, expected_seq, 0, b''), client_addr)
            expected_seq += 1

        else:
            send_packet(server_socket, create_packet(0, expected_seq - 1