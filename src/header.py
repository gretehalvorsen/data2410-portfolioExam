# Import necessary libraries
from struct import *


# Define the format for the packet header, which consists of 3 unsigned short integers (each represented by 'H').
header_format = '3H' 

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