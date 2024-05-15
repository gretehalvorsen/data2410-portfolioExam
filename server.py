import socket
import datetime
import time
from header import create_packet, send_packet, receive_packet
"""
    server() function acts as a UDP server, receiving data from a client

    It takes in args: A namespace containing the command-line arguments,
    and use the following attributes: 
              - ip: The IP address to bind the server to.
              - port: The port number to bind the server to.
              - file: The name of the file to write the received data to. If not provided, defaults to "image.jpg".
              - discard: The sequence number of a packet to be discarded for testing purposes.

    It does not return anything, but writes the received data to file
    """

def server(args):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((args.ip, args.port))
    total_data = 0  # initialize total data
    serving_client = False  # add this line
    client_addr_serving = None  # keep track of the client being served

    #If no filename is given in argument it is named image.jpg
    if args.file is None:
        received_file = open("image.jpg", "wb")
    else:
        received_file = open(args.file, "wb")

    expected_seq = 1  # Initialize expected sequence number
    discard_seq = args.discard #Set sequence number to be discarded if --discard flag i used

    while True:  
    # Calls receive_packet function to receive a packet from the client. 
        msg, client_addr, seq, ack, syn, ack_flag, fin = receive_packet(server_socket)

        #Test to see if the server already has a connection with a client
        if serving_client and client_addr != client_addr_serving:
            continue  # skip this loop iteration if another client is trying to connect

        if syn:  # If the SYN flag of the received packet is set
            start_time = time.time()  # initialize start time
            serving_client = True  # set serving_client to True when a client connects
            client_addr_serving = client_addr  # keep track of the client being served
            print("SYN packet is received.")  # Print a message indicating a SYN packet is received
            syn_ack_packet = create_packet(0, 0, 12, b'')  # Create a packet with both SYN and ACK flags set (8 | 4)
            send_packet(server_socket, syn_ack_packet, client_addr)  # Send the SYN-ACK packet back to the client
            print(f'SYN-ACK packet is sent')  # Print a message indicating a SYN-ACK packet is sent

        elif fin:  # If the FIN flag of the received packet is set
            end_time = time.time()  # End time of the file transfer
            serving_client = False  # set serving_client to False when the client disconnects
            print("\nFIN packet is received.")  # Print a message indicating a FIN packet is received
            fin_ack_packet = create_packet(0, 0, 6, b'') # Create a packet with both ACK and FIN flags set (4 | 2 )
            send_packet(server_socket, fin_ack_packet, client_addr)  # Send the FIN-ACK packet back to the client
            received_file.close()  # Close the file
            print(f'FIN ACK packet is sent')
            break  # Break the loop as the file transfer is complete

        
        elif ack_flag:  # If the ACK flag of the received packet is set
            print(f'ACK packet is received')
            print('Connection established')
            start_time = time.time() #Starting the timer after the connection is established
            continue
            
        # How the server receives data from client
        elif seq == expected_seq:  # Check if the sequence number is the expected one
            if seq == discard_seq: # Check if the sequence number is the one to be discarded
                discard_seq = None  # Reset the discard value so the packet isn't skipped again
                continue 

            print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Packet {seq} is received")
            if not (syn or fin or ack_flag): 
                received_file.write(msg[6:])  # Write the data to the file
                ack_packet = create_packet(0, seq, 4, b'')  # Create ACK packet
                send_packet(server_socket, ack_packet, client_addr)  # Send ACK packet
                print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Sending ACK for the received {seq}")
                expected_seq += 1  # Increment expected sequence number
                last_ack = seq  # Update the last acknowledged sequence number
                total_data += len(msg)        
                
        else:  # If an out-of-order packet is received
            print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- out-of-order packet {seq} is received")
            ack_packet = create_packet(0, last_ack, 4, b'')  # Create ACK packet for the last correctly received packet
            send_packet(server_socket, ack_packet, client_addr) 
            print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Sending ACK for the received {last_ack}")
               
    duration = end_time - start_time  # Total time taken for the file transfer
    throughput = (total_data * 8) / (1000 * 1000 * duration)  # Calculate throughput in Mbps
    print(f"\nThe throughput is {throughput:.2f} Mbps")
    print(f'Connection Closes') 
    server_socket.close()