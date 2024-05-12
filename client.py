import socket
import queue
import datetime
from header import create_packet, send_packet, recv_packet

def client(args):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(0.5)
    print()
    print("Connection Establishment Phase:")
    print()
    syn_packet = create_packet(0, 0, 8, b'')# Packet with SYN flag. 
    send_packet(client_socket, syn_packet, (args.ip, args.port))# Sending the packet with to the server.
    print(f'SYN packet it sent')

# Start of the three way handshake
    while True:
        try:
            msg, server_addr, seq, ack, syn, ack_flag, fin = recv_packet(client_socket)
            if syn and ack_flag:
                print("SYN-ACK packet is received")  # Print a message indicating a SYN-ACK packet is received
                ack_packet = create_packet(0, 0, 4, b'')  # Create a packet with ACK flag set
                send_packet(client_socket, ack_packet, server_addr)  # Send the ACK packet to complete the three-way handshake
                print("ACK packet is sent.")  # Print a message indicating an ACK packet is sent
                break
        except socket.timeout:
            print()
            print("Connection failed")
            exit(1)
        
        #End of the three way handshak

        # File transfer part
    print()
    print(f'Data Transfer:')
    print('')

    # Initialize sequence number and sliding window
    base = 1
    next_seq = 1
    window = args.window
    sliding_window = queue.Queue()
    eof = False

    # Open the file in binary mode
    with open(args.file, 'rb') as f:
        while not eof or not sliding_window.empty():
            while next_seq < base + window and not eof:
                data = f.read(994)
                if not data:
                    eof = True
                else:
                    data_packet = create_packet(next_seq, 0, 0, data)
                    send_packet(client_socket, data_packet, (args.ip, args.port))
                    sliding_window.put((next_seq, data_packet))
                    seq_nums = [str(seq) for seq, _ in list(sliding_window.queue)]
                    print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Packet with seq = {next_seq} is sent. Sliding window:  {', '.join(seq_nums)}")
                    next_seq += 1

            if sliding_window.empty():
                break
            try:
                _, _, seq, ack, _, ack_flag, _ = recv_packet(client_socket)
                if ack_flag:  
                    print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- ACK for packet = {ack} is received")
                    # Only remove the packet from the window when an ACK specifically for it is received
                    if not sliding_window.empty() and sliding_window.queue[0][0] == ack:
                        sliding_window.get()  
                        base += 1
                    # If a duplicate ACK is received, retransmit all packets in the window
                        #Er denne nødvendig???
                    else:
                        print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Duplicate ACK received. Retransmitting all packets in the window.")
                        for seq, packet in sliding_window.queue:
                            send_packet(client_socket, packet, (args.ip, args.port))
                            print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Packet with seq = {seq} is resent.")

            except socket.timeout:
                print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Timeout occurred") 
                # If a timeout occurs, retransmit all packets in the window
                for seq, packet in sliding_window.queue:
                    send_packet(client_socket, packet, (args.ip, args.port))
                    print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Retransmitting packet with seq = {seq}")
    print(f'DATA finished')
    print()                 
    print()
    print('Connection Teardown:')
    print()
    # Create a packet with the FIN flag set
    fin_packet = create_packet(0, 0, 2, b'') 
    print('FIN packet is sent')
    # Send the FIN packet to the server
    send_packet(client_socket, fin_packet, (args.ip, args.port))
    # Start of teardown
    while True:
        try:
            _, server_addr, seq, ack, syn, ack_flag, _ = recv_packet(client_socket)
            if ack_flag:
                print("FIN-ACK packet is received.")  # Print a message indicating a SYN-ACK packet is received
                print('Connection closes')
                client_socket.close()
                break
        except socket.timeout:
            print("Timeout waiting for FIN-ACK packet. C.")
            send_packet(client_socket, fin_packet, (args.ip, args.port))
        #Teardown complete