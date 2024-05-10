import socket
import queue
import datetime
from header import create_packet, send_packet, recv_packet, send_ack


def client(args):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(5)
    print("Connection Establishment Phase:")
    print()
    syn_packet = create_packet(0, 0, 8, b'')# Packet with SYN flag. 
    send_packet(client_socket, syn_packet, (args.ip, args.port))# Sending the packet with to the server.
    print(f'SYN packet it sent')

# Start of the three way handshak
    while True:
        try:
            msg, server_addr, seq, ack, syn, ack_flag, fin = recv_packet(client_socket)
            if syn and ack_flag:
                print("SYN-ACK packet is received.")  # Print a message indicating a SYN-ACK packet is received
                ack_packet = create_packet(0, 0, 4, b'')  # Create a packet with ACK flag set
                send_packet(client_socket, ack_packet, server_addr)  # Send the ACK packet to complete the three-way handshake
                print("ACK packet is sent.")  # Print a message indicating an ACK packet is sent
                break
        except socket.timeout:
            print("Timeout waiting for SYN-ACK packet. Resending SYN packet.")
            send_packet(client_socket, syn_packet, (args.ip, args.port))
        #End of the three way handshak


    # File transfer part
    print(f'Data Transfer:')
    print('')
    
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
            msg, server_addr, seq, ack, syn, ack_flag, fin = recv_packet(client_socket)
            if ack_flag:
                print("FIN-ACK packet is received.")  # Print a message indicating a SYN-ACK packet is received
                print('Connection closes')
                client_socket.close()
                break
        except socket.timeout:
            print("Timeout waiting for FIN-ACK packet. C.")
            send_packet(client_socket, fin_packet, (args.ip, args.port))
        #Teardown complete
