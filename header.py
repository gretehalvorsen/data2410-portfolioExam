# Import required libraries
from struct import *

# Define the format for the header
header_format = '3H' # The format is 3 unsigned short integers

# Function to create a data packet
def create_packet(seq, ack, flags, data):
    # Pack the sequence number, acknowledgment number, and flags into a binary data
    header = pack(header_format, seq, ack, flags) 
    # Combine the header and the actual data to form the complete packet
    packet = header + data
    # Return the final packet
    return packet

# Function to parse the header of the packet
def parse_header(header):
    # Unpack the header to get the sequence number, acknowledgment number, and flags
    seq, ack, flags = unpack(header_format, header)
    # Return these values
    return seq, ack, flags 

# Function to send a packet over a socket to a specified address
def send_packet(socket, packet, addr):
    # Use the socket's sendto method to send the packet to the given address
    socket.sendto(packet, addr)

# Function to receive a packet from a socket
def recv_packet(socket, size=1000):
    # Use the socket's recvfrom method to receive a packet, the default size is 1000 bytes
    msg, addr = socket.recvfrom(size)
    # Parse the header of the received message
    seq, ack, flags = parse_header(msg[:6])
    syn, ack_flag, fin = parse_flags(flags)
    # Return the message, sender's address, sequence number, acknowledgment number, and flags
    return msg, addr, seq, ack, syn, ack_flag, fin

def parse_flags(flags):
    syn = flags & (1 << 3)
    ack = flags & (1 << 2)
    fin = flags & (1 << 1)
    return syn, ack, fin

# The function sends a packet with ACK flag. 
def send_ack(socket, seq, addr):
    ack_packet = create_packet(0, 0, 4, b'')
    send_packet(socket, ack_packet, addr)

# The function used in the client side to recive the ack. 
def recv_ack(socket):
    try:
        msg, addr, seq, ack, syn, ack_flag, fin = recv_packet(socket)
        if ack_flag:
            return ack, addr
        else:
            return None, None
    except socket.timeout:
        return None, None          