

while True:
    # Receive data
    data, address = server.recvfrom(1024)
    
    if data.decode('utf-8') == 'SYN':
        print("SYN packet is received")
        sent = server.sendto(b"SYN-ACK", address)
        print("SYN-ACK packet is sent")
        
    elif data.decode('utf-8') == 'ACK':
        print("ACK packet is received")
        print("Connection established")
    else:
        print("Connection failed")   
