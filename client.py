import socket
import queue
import datetime
from header import create_packet, send_packet, receive_packet

'''
client(args) function performs the client side operations of 
a file transfer protocol over UDP sockets. It implements a three-way handshake 
to establish a connection, transfers a file using gobackn with a sliding window protocol, 
and ends the connection using a teardown process.

It takes in args: A namespace containing the command-line arguments. 
And use the following attributes:
-- file: The name of the file to be transferred
-- ip: The IP address of the server
-- port: The port number of the server
-- window: The size of the sliding window

The function does not return a value. Instead, it sends packets over the network 
and prints information about the file transfer process to the standard output

Exception handles socket.timeout exceptions, which occur when the socket's recv() 
method blocks for more than the specified timeout period. When such an exception 
is caught, the function retransmits all packets currently in the sliding window
'''
def client(args):
    if args.file is None:
        print("Error: You must specify a file to send when using client mode.")
        return
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(0.5)
    print("\nConnection Establishment Phase:\n")
    syn_packet = create_packet(0, 0, 8, b'')# Packet with SYN flag. 
    send_packet(client_socket, syn_packet, (args.ip, args.port))# Sending the packet with to the server.
    print(f'SYN packet it sent')
# Start of the three way handshake
    while True:
        try:
            msg, server_addr, seq, ack, syn, ack_flag, fin = receive_packet(client_socket)
            if syn and ack_flag:
                print("SYN-ACK packet is received")  # Print a message indicating a SYN-ACK packet is received
                ack_packet = create_packet(0, 0, 4, b'')  # Create a packet with ACK flag set
                send_packet(client_socket, ack_packet, server_addr)  # Send the ACK packet to complete the three-way handshake
                print("ACK packet is sent.")  # Print a message indicating an ACK packet is sent
                break
        except socket.timeout:
            print("\nConnection failed")
            exit(1)
        #End of the three way handshake

        # File transfer part
    print(f'\nData Transfer:\n')
    

    # Initialize sequence number and sliding window
    base = 1  # The base of the sliding window
    nextseqnum = 1  # The next sequence number to be used
    window = args.window  # The size of the sliding window
    sliding_window = queue.Queue()  # The sliding window, implemented as a queue
    eof = False  # A flag indicating if we have reached the end of the file

    # Open the file in binary mode
    with open(args.file, 'rb') as f:
        # Keep looping until we reach the end of the file and the sliding window is empty
        while not eof or not sliding_window.empty():
            # Keep sending packets until the sliding window is full or we reach the end of the file
            while nextseqnum < base + window and not eof:
                # Read a chunk of data from the file
                data = f.read(994)
                if not data:
                    # If no data is read (i.e., we have reached the end of the file), set eof to True
                    eof = True
                else:
                    # Create a packet with the data and send it
                    data_packet = create_packet(nextseqnum, 0, 0, data)
                    send_packet(client_socket, data_packet, (args.ip, args.port))
                    # Add the packet to the sliding window
                    sliding_window.put((nextseqnum, data_packet))
                    # Print a message indicating the packet has been sent and show the current state of the sliding window
                    seq_nums = [str(seq) for seq, _ in list(sliding_window.queue)]
                    print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Packet with seq = {nextseqnum} is sent. Sliding window:  {', '.join(seq_nums)}")
                    # Increment the sequence number
                    nextseqnum += 1

            # If the sliding window is empty (i.e., all packets have been acknowledged), break the loop
            if sliding_window.empty():
                break
            try:
                # Try to receive a packet
                _, _, seq, ack, _, ack_flag, _ = receive_packet(client_socket)
                if ack_flag:  
                    # If the packet is an acknowledgment, print a message and update the sliding window
                    print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- ACK for packet = {ack} is received")
                    # Only remove the packet from the window when an ACK specifically for it is received
                    if not sliding_window.empty() and sliding_window.queue[0][0] == ack:
                        sliding_window.get()  
                        base += 1
                    # If a duplicate ACK is received, retransmit all packets in the window
                    else:
                        print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Duplicate ACK received.")
                        for seq, packet in sliding_window.queue:
                            send_packet(client_socket, packet, (args.ip, args.port))
                            print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Packet with seq = {seq} is resent.")

            except socket.timeout:
                # If a timeout occurs, print a message and retransmit all packet in the window
                print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Timeout occurred") 
                for seq, packet in sliding_window.queue:
                    send_packet(client_socket, packet, (args.ip, args.port))
                    print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Retransmitting packet with seq = {seq}")
    # Print a message indicating the end of the data transfer
    print(f'DATA finished\n')

    # Start of teardown
    print('\nConnection Teardown:\n')
    # Create a packet with the FIN flag set
    fin_packet = create_packet(0, 0, 2, b'') 
    print('FIN packet is sent')
    send_packet(client_socket, fin_packet, (args.ip, args.port))
    while True:
        try:
            _, server_addr, seq, ack, syn, ack_flag, _ = receive_packet(client_socket)
            if ack_flag:
                print("FIN-ACK packet is received.")  
                print('Connection closes')
                client_socket.close()
                break
        except socket.timeout:
            print("Timeout waiting for FIN-ACK packet. Closing the connection.")
            client_socket.close()
            break
    #Teardown complete