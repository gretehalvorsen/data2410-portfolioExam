# Import necessary libraries
from struct import *


# Define the format for the packet header, which consists of 3 unsigned short integers (each represented by 'H').
header_format = '3H' 


'''
Create_packet function creates a packet with a header and data.
Packs the sequence number, acknowledgment number, and flags into 
a binary string (header) and combines it with the data to form the 
complete packet.

Arguments:
seq: The sequence number for the packet.
ack: The acknowledgment number for the packet.
flags: An integer representing the flags (SYN, ACK, FIN) for the packet.
data: The actual data or payload of the packet.

Returns the final packet as a combination of the header and data.
'''
def create_packet(seq, ack, flags, data):
    # Pack the sequence number, acknowledgment number, and flags into a binary string (header).
    header = pack(header_format, seq, ack, flags) 
    # Combine the header with the actual data to form the complete packet.
    packet = header + data
    # Return the final packet.
    return packet


'''
parse_header() function parses the header of a packet.
It unpacks the binary string to get the sequence number, 
acknowledgment number, and flags

Arguments:
header: The header of the packet as a binary string.

It returns sequence number, acknowledgment number, and flags as separate variables.
'''
def parse_header(header):
    # Unpack the binary string (header) to get the sequence number, acknowledgment number, and flags.
    seq, ack, flags = unpack(header_format, header)
    # Return these values.
    return seq, ack, flags 


'''
send_packet() function sends a packet over a socket to a specified address.
It uses the sendto method of the socket object to send the packet to a given address.

Arguments:
socket: The socket over which to send the packet.
packet: The packet to be sent.
addr: The address to which the packet is sent.
'''
# Function to send a packet over a socket to a specified address.
def send_packet(socket, packet, addr):
    # Use the sendto method of the socket object to send the packet to the given address.
    socket.sendto(packet, addr)


'''
recv_packet() function receives a packet from a socket.
Uses the recvfrom method of the socket object to receive 
a packet and parses the header of the received message.

Arguments:
socket: The socket from which to receive the packet.
size: The size of the packet to receive. By default, it's 1000 bytes.

Return the message, sender's address, sequence number, acknowledgment number, and flags.
'''    
def recv_packet(socket, size=1000):
    # Use the recvfrom method of the socket object to receive a packet. The default size of the packet is 1000 bytes.
    msg, addr = socket.recvfrom(size)
    # Parse the header of the received message to get the sequence number, acknowledgment number, and flags.
    seq, ack, flags = parse_header(msg[:6])
    # Parse the flags to get the SYN, ACK, and FIN flags.
    syn, ack_flag, fin = parse_flags(flags)
    # Return the message, sender's address, sequence number, acknowledgment number, and flags.
    return msg, addr, seq, ack, syn, ack_flag, fin


'''
parse_flags() function parses the flags.
Checks each bit in the flags integer using bitwise 
operations to get the SYN, ACK, and FIN flags.

Arguments:
flags: An integer representing the flags.

Returns the SYN, ACK, and FIN flags as separate variables.
'''
def parse_flags(flags):
    # Each flag is represented by a bit in the flags integer. Check each bit using bitwise operations.
    syn = flags & (1 << 3)
    ack = flags & (1 << 2)
    fin = flags & (1 << 1)
    # Return the flags.
    return syn, ack, fin



'''send_ack() function creates an ACK packet
 and sends it over the socket to the given address.

Arguments:
socket: The socket over which to send the ACK.
seq: The sequence number for the ACK.
addr: The address to which the ACK is sent.
'''
def send_ack(socket, seq, addr):
    # Create an ACK packet. The sequence number and acknowledgment number are 0, the flags integer is 4 (which represents an ACK), and there's no data.
    ack_packet = create_packet(0, 0, 4, b'')
    # Send the ACK packet.
    send_packet(socket, ack_packet, addr)



'''
recv_ack() function receives a packet and checks if it's an ACK. 
If a timeout occurs while waiting to receive a packet, it returns None for both values.

Arguments:
socket: The socket from which to receive the ACK.

If the packet is an ACK, it returns the acknowledgment number and sender's address. 
If it is not an ACK or if a timeout occurs, it returns None for both values.

Exception: If a socket.timeout exception occurs, it returns None for both values. This means that 
the function will not raise an exception if a timeout occurs; instead, it will handle it and return None
'''
# Function to receive an ACK in the client side.
def recv_ack(socket):
    try:
        # Receive a packet.
        msg, addr, seq, ack, syn, ack_flag, fin = recv_packet(socket)
        # If the packet is an ACK (ack_flag is True), return the acknowledgment number and sender's address.
        if ack_flag:
            return ack, addr
        # If the packet is not an ACK, return None for both values.
        else:
            return None, None
    # If a timeout occurs while waiting to receive a packet, return None for both values.
    except socket.timeout:
        return None, None