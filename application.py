from server import server
from client import client
import argparse


parser = argparse.ArgumentParser(description='File Transfer Application')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-s", "--server", action="store_true", help="enable the server mode")
group.add_argument("-c", "--client", action="store_true", help="enable the client mode")

parser.add_argument("-i", "--ip", type=str, default="127.0.0.1",
                        help="bind the ip address at the server side or select server's ip at the client side")
parser.add_argument("-p", "--port", type=int, default=8088, choices=range(1024, 65536),
                        help="select port number on which the server should listen or the server's port number at the client side")
parser.add_argument("-f", "--file", type=str, help="choose the jpg file")
parser.add_argument("-w", "--window", type=int, default=3, help="sliding window size")
parser.add_argument("-d", "--discard", type=int, help="skip a seq to check for retransmission")

# Parse the arguments and store them in 'args'
args = parser.parse_args()

if args.server:
    server(args.ip, args.port)
elif args.client:
    client(args.ip, args.port, args.file, args.window, args.discard)

