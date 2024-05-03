import time
import socket

# Sender side
def sender(sock, addr, data, N):
    base = 0  # Base of the window
    nextseqnum = 0  # Next sequence number
    buffer = {}  # Store the sent data

    # While there's data to be sent
    while base < len(data):
        # Send data that fits into the window
        while nextseqnum < base + N and nextseqnum < len(data):
            # Prepare the message, with sequence number and data
            msg = '%d %s' % (nextseqnum, data[nextseqnum])
            # Send the message
            sock.sendto(msg.encode(), addr)
            # Store the message in the buffer
            buffer[nextseqnum] = data[nextseqnum]
            # Increase the sequence number
            nextseqnum += 1

        # Wait for acknowledgments
        sock.settimeout(0.2)  # Set a timeout for waiting acks
        try:
            while True:
                # Receive ack
                ack, addr = sock.recvfrom(1024)
                # Extract the sequence number from the ack
                ack = int(ack.decode().split()[1])

                # If the ack is for the base, move the window
                if ack >= base:
                    base = ack + 1
        except socket.timeout:
            # If timeout occurs, resend the data
            pass

# Receiver side
def receiver(sock, addr, N):
    expectedseqnum = 0  # Expected sequence number
    buffer = {}  # Store the received data

    # Always waiting for new packets
    while True:
        # Receive a packet
        msg, addr = sock.recvfrom(1024)
        # Extract the sequence number and data from the packet
        seqnum, data = msg.decode().split(' ', 1)
        seqnum = int(seqnum)

        # If the sequence number is the expected one
        if seqnum == expectedseqnum:
            # Print the data
            print('Received', data)
            # Send an ack for the received packet
            sock.sendto(('ACK %d' % expectedseqnum).encode(), addr)
            # Expect the next sequence number
            expectedseqnum += 1
        # If the packet is out of order
        elif seqnum in buffer:
            # Send an ack for the last in-order packet
            sock.sendto(('ACK %d' % (seqnum - 1)).encode(), addr)
        else:
            # Store the out-of-order packet for later use
            buffer[seqnum] = data