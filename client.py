import socket

def client(ip, port, file, window, discard):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(5)  # Set timeout to 5 seconds
    server_address = (ip, port)

    print("Connection Establishment Phase:")
    print()

    # Send data
    message = b'SYN'
    sent = client.sendto(message, server_address)
    print("SYN packet is sent")

    try:
        # Receive response
        data, server = client.recvfrom(1024)
        if data == b"SYN-ACK":
            print("SYN-ACK packet is received")
            sent = client.sendto(b"ACK", server_address)
            print("ACK packet is sent")
            print("Connection established")

        # Send 'START' packet before starting the file transfer.
        client.sendto(b"START", server_address)

        # Start file transfer
        print("File Transfer Phase:")
        print()

        with open(file, 'rb') as image:
                while (data := image.read(994)):
                    client.sendto(data, server_address)
                print("Image sent.")

    except socket.timeout:
        print("Connection failed")   

