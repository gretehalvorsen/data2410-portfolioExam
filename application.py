from server import server
from client import client
import argparse
import re
from struct import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--client", action="store_true", help="Run as client.")
    parser.add_argument("-s", "--server", action="store_true", help="Run as server.")
    parser.add_argument('-i', '--ip', type=str, default="127.0.0.1", help='Server IP address.')
    parser.add_argument("-f", "--file", type=str, help="File to transfer.")
    parser.add_argument('-p', '--port', default=8088, type=int, help='Server port number.')
    parser.add_argument('-w', '--window_size', default=3, type=int, help="The window size")
    args = parser.parse_args()

    # Check the arguments. If both server and client modes are enabled, print an error message
    if args.server and args.client:
        print('You cannot run server and client at the same time')

    # If server mode is enabled, set the mode to 'server'
    elif args.server:
        mode = 'server'
        server(args)

# If client mode is enabled, set the mode to 'client'
    elif args.client:
        mode = 'client'
        client(args)

# If neither mode is enabled, print an error message and exit
    else:
        print('You must run either in server or client mode')
        exit(1)

# Check if the port is valid. If not, print an error message and exit
    if not 1024 <= args.port <= 65535:
        print('Invalid port. It must be within the range [1024,65535]')
        exit(1)

    # Check if the ip is valid using a regular expression. 
    if re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', args.ip):
        # Split the IP address into four parts
        ip_parts = args.ip.split('.')
        # Check if each part is a number between 0 and 255
        if not all(0 <= int(part) <= 255 for part in ip_parts):
            print('Invalid IP. Each block must be in the range [0,255]')
            exit(1)
    else:
        print('Invalid IP. It must be in this format: 10.1.2.3')
        exit(1)

    # Check if the file is a .jpg using a regular expression.
    if args.file is not None:
        if not re.match(r'.*\.jpg$', args.file):
            print("Invalid file, must be a .jpg file.")  # Replace with your error message
            return
            

if __name__ == "__main__":
    main()
