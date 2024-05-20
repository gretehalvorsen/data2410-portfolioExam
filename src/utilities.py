from header import *
from struct import *

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
send_packet() function sends a packet over a socket to a specified address.
It uses the sendto method of the socket object to send the packet to a given address.

Arguments:
    socket: The socket over which to send the packet.
    packet: The package to be sent.
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
def receive_packet(socket, size=1000):
    # Use the recvfrom method of the socket object to receive a packet. The default size of the packet is 1000 bytes.
    msg, addr = socket.recvfrom(size)
    # Parse the header of the received message to get the sequence number, acknowledgment number, and flags.
    seq, ack, flags = parse_header(msg[:6])
    # Parse the flags to get the SYN, ACK, and FIN flags.
    syn, ack_flag, fin = parse_flags(flags)
    # Return the message, sender's address, sequence number, acknowledgment number, and flags.
    return msg, addr, seq, ack, syn, ack_flag, fin