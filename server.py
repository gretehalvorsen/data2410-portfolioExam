import socket
import struct

def server(ip, port):
    # Create a new socket using the given address family (AF_INET) and socket type (SOCK_DGRAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Assigning static IP and port values
    port = 8000
    server_ip = '127.0.0.1'
    
    # Bind the socket to the address (ip and port)
    sock.bind((ip, port))
    
    # Print a ready message
    print('The server is ready')
    
    # This line seems out of place since 'serverSocket' is not defined anywhere
    serverSocket.listen()
    
    # Set a timeout period on blocking socket operations
    sock.settimeout(0.5)

    # Receive data from the socket, up to a maximum of 1024 bytes
    data, addr = sock.recvfrom(1024)
    
    # Check if received data is as expected for connection establishment
    if data != b'SYN':
        raise Exception('Failed to establish connection')
    
    # Send acknowledgment for SYN packet
    sock.sendto(b'SYN-ACK', addr)
    print('SYN-ACK packet is sent')

    # Receive next packet
    data, addr = sock.recvfrom(1024)
    
    # Check if received data is as expected for connection establishment
    if data != b'ACK':
        raise Exception('Failed to establish connection')
    print('ACK packet is received')

    print('Connection established')

    # Open a file to write the received data
    with open('output_file', 'wb') as file:
        expected_seq_num = 0
        while True:
            try:
                # Receive data from the socket
                data, addr = sock.recvfrom(1024)
                
                # Unpack received data
                seq_num, length = struct.unpack('!II', data[:8])

                # Check if the sequence number is as expected
                if seq_num == expected_seq_num:
                    # Check if the length of data matches the received length
                    if length != len(data[8:]):
                        print('Packet length mismatch, packet possibly corrupt')
                        continue

                    # Write data to file
                    file.write(data[8:])

                    # Pack the sequence number into a binary string
                    ack_data = struct.pack('!I', seq_num)
                    
                    # Send acknowledgment for received packet
                    sock.sendto(ack_data, addr)
                    print(f'Packet {seq_num} is received, sending ack for the received {seq_num}')

                    # Increase the expected sequence number
                    expected_seq_num += 1

            # Handle socket timeout exception
            except socket.timeout:
                print('Socket timed out, ending file reception')
                break

    # Receive final packet
    data, addr = sock.recvfrom(1024)
    
    # Check if received data is as expected for connection termination
    if data != b'FIN':
        raise Exception('Failed to close connection')
    
    # Send acknowledgment for FIN packet
    sock.sendto(b'FIN-ACK', addr)
    print('FIN ACK packet is sent')

    print('Connection closed')