import socket
import datetime
import time
from header import create_packet, send_packet, recv_packet, send_ack

def server(args):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((args.ip, args.port))
    total_data = 0  # initialize total data
    start_time = time.time()

    if args.file is None:
        recvd_file = open("image.jpg", "wb")
    else:
        recvd_file = open(args.file, "wb")

    expected_seq = 1  # Initialize expected sequence number
    discard_seq = args.discard
    last_ack = 0

    while True:  # Starts an infinite loop
    # Calls recv_packet function to receive a packet from the client. 
    # The returned values are stored in variables: msg (message), client_addr (client address), seq (sequence number), 
    # ack (acknowledgment number), syn (SYN flag), ack_flag (ACK flag), fin (FIN flag)
        msg, client_addr, seq, ack, syn, ack_flag, fin = recv_packet(server_socket)

        if syn:  # If the SYN flag of the received packet is set
            start_time = time.time()  # initialize start time
            print("SYN packet is received.")  # Print a message indicating a SYN packet is received
            syn_ack_packet = create_packet(0, 0, 12, b'')  # Create a packet with both SYN and ACK flags set (8 | 4)
            send_packet(server_socket, syn_ack_packet, client_addr)  # Send the SYN-ACK packet back to the client
            print(f'SYN-ACK packet is sent')  # Print a message indicating a SYN-ACK packet is sent

        elif fin:  # If the FIN flag of the received packet is set
            print("FIN packet is received.")  # Print a message indicating a FIN packet is received
            fin_ack_packet = create_packet(0, 0, 6, b'') # Create a packet with both ACK and FIN flags set (4 | 2 )
            send_packet(server_socket, fin_ack_packet, client_addr)  # Send the FIN-ACK packet back to the client
            recvd_file.close()  # Close the file
            print(f'FIN ACK packet is sent')
            break  # Break the loop as the file transfer is complete

        elif ack_flag:  # If the ACK flag of the received packet is set
            print(f'ACK packet is received')
            print('Connection established')
            continue  # Continue to the next iteration of the loop without executing the rest of the code in the loop


        elif seq == expected_seq:  # If the sequence number is the expected one
            if seq == discard_seq:
                discard_seq = None  # Reset the discard value so the packet isn't skipped again
                continue  # Skip the rest of the loop for this packet

            print(f'{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Packet {seq} is received')
            if not (syn or fin or ack_flag): 
                recvd_file.write(msg[6:])  # Write the data to the file
                ack_packet = create_packet(0, seq, 4, b'')  # Create ACK packet
                send_packet(server_socket, ack_packet, client_addr)  # Send ACK packet
                print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- Sending ACK for the received {seq}")
                expected_seq += 1  # Increment expected sequence number
                last_ack = seq  # Update the last acknowledged sequence number
                total_data += len(msg)

        else:  # If an out-of-order packet is received
            print(f'{datetime.datetime.now().strftime('%H:%M:%S.%f')} -- out-of-order packet {seq} is received')    
    
    end_time = time.time()  # End time of the file transfer
    elapsed_time = end_time - start_time  # Total time taken for the file transfer
    print(f"Total elapsed time: {elapsed_time} seconds")  # Print total elapsed time
    throughput = (total_data * 8) / (1000 * 1000 * elapsed_time)  # Throughput in Mbps
    print(f"The throughput is {throughput:.2f} Mbps")
    print(f'Connection Closes') 
    server_socket.close()