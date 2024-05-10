import socket
import datetime
import time
from header import create_packet, send_packet, recv_packet, send_ack

def server(args):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((args.ip, args.port))
    start_time = None  # initialize start time
    total_data = 0  # initialize total data

    if args.file is None:
        recvd_file = open("image.jpg", "wb")
    else:
        recvd_file = open(args.file, "wb")

    while True:  # Starts an infinite loop
    # Calls recv_packet function to receive a packet from the client. 
    # The returned values are stored in variables: msg (message), client_addr (client address), seq (sequence number), 
    # ack (acknowledgment number), syn (SYN flag), ack_flag (ACK flag), fin (FIN flag)
        msg, client_addr, seq, ack, syn, ack_flag, fin = recv_packet(server_socket)

        if syn:  # If the SYN flag of the received packet is set
            print("SYN packet is received.")  # Print a message indicating a SYN packet is received
            syn_ack_packet = create_packet(0, 0, 12, b'')  # Create a packet with both SYN and ACK flags set (8 | 4)
            send_packet(server_socket, syn_ack_packet, client_addr)  # Send the SYN-ACK packet back to the client
            print(f'SYN-ACK packet is sent')  # Print a message indicating a SYN-ACK packet is sent

        elif fin:  # If the FIN flag of the received packet is set
            print("FIN packet is received.")  # Print a message indicating a FIN packet is received
            recvd_file.close()  # Close the file that was being written to
            fin_ack_packet = create_packet(0, 0, 6, b'') # Create a packet with both ACK and FIN flags set (4 | 2 )
            send_packet(server_socket, fin_ack_packet, client_addr)  # Send the FIN-ACK packet back to the client
            print(f'FIN ACK packet is sent')
            break  # Break the loop as the file transfer is complete

        elif ack_flag:  # If the ACK flag of the received packet is set
            print(f'ACK packet is received')
            print('Connection established')
            continue  # Continue to the next iteration of the loop without executing the rest of the code in the loop

    
   #end_time = time.time()  # ends the timer
   # elapsed_time = end_time - start_time  # calculates the elapsed time
   # throughput = (total_data * 8) / (1000 * 1000 * elapsed_time)  # calculates the throughput in Mbps
    #print('')
    #print(f"The throughput is {throughput:.2f} Mbps")  

    print(f'Connection Closes') 
    server_socket.close()
    