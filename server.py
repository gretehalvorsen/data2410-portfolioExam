import socket

def server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((ip, port))

    # Open a file to write the incoming data.
    image = open('received_image.jpg', 'wb')

    while True:
        # Receive data
        data, address = server.recvfrom(994)
        
        # Try to decode the data as UTF-8 text.
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            # If the data cannot be decoded as text, it's part of the file.
            image.write(data)
            continue

        # Handle the different types of text packets.
        if text == 'SYN':
            print("SYN packet is received")
            sent = server.sendto(b"SYN-ACK", address)
            print("SYN-ACK packet is sent")
            
        elif text == 'ACK':
            print("ACK packet is received")
            print("Connection established")

            # Start file transfer.
            print("File Transfer Phase:")
            print()

        elif text == 'START':
            # A 'START' packet signals the start of the file transfer.
            print("Starting file transfer")

        else:
            print("Connection failed")   

    # Close the file and the socket.
    image.close()
    server.close()