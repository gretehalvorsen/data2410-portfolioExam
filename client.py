import socket

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 9999)

print("Connection Establishment Phase:")
print()

# Send data
message = b'SYN'
sent = client.sendto(message, server_address)
print("SYN packet is sent")

# Receive response
data, server = client.recvfrom(1024)
if data == b"SYN-ACK":
    print("SYN-ACK packet is received")
    sent = client.sendto(b"ACK", server_address)
    print("ACK packet is sent")
    print("Connection established")
else:
    print("Connection failed")
    #print(f"received {data} from {server}")

