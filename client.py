import socket
import struct
import time

def client(ip, port, filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.5)

    sock.sendto(b'SYN', (ip, port))
    print('SYN packet is sent')

    data, addr = sock.recvfrom(1024)
    if data != b'SYN-ACK':
        raise Exception('Failed to establish connection')
    print('SYN-ACK packet is received')

    sock.sendto(b'ACK', (ip, port))
    print('ACK packet is sent')

    print('Connection established')

    start_time = time.time()
    total_bytes = 0
    window_size = 5
    base = 0
    next_seq_num = 0
    buffer = {}

    with open(filename, 'rb') as file:
        while True:
            if next_seq_num < base + window_size:
                data = file.read(1024)
                if not data:
                    break
                total_bytes += len(data)

                header = struct.pack('!II', next_seq_num, len(data))
                buffer[next_seq_num] = header + data
                sock.sendto(buffer[next_seq_num], (ip, port))
                print(f'Packet with seq = {next_seq_num} is sent, sliding window = {[i for i in range(base, next_seq_num+1)]}')

                next_seq_num += 1
            else:
                try:
                    ack_data, addr = sock.recvfrom(1024)
                    ack_seq_num = struct.unpack('!I', ack_data)[0]
                    base = max(base, ack_seq_num + 1)
                except socket.timeout:
                    for seq_num in range(base, next_seq_num):
                        sock.sendto(buffer[seq_num], (ip, port))
                        print(f'Packet with seq = {seq_num} is sent, sliding window = {[i for i in range(base, seq_num+1)]}')

    end_time = time.time()
    transfer_time = end_time - start_time
    throughput = total_bytes / transfer_time
    print(f'Throughput: {throughput * 8 / (1024*1024):.2f} Mbps')

    sock.sendto(b'FIN', (ip, port))
    print('FIN packet is sent')

    data, addr = sock.recvfrom(1024)
    if data != b'FIN-ACK':
        raise Exception('Failed to close connection')
    print('FIN ACK packet is received')

    print('Connection closed')

