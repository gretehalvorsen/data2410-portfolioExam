from server import server
from client import client
import argparse
import re
from struct import *
"""
    This function parses command-line arguments and runs as a server or client based on these arguments.

    Exceptions:
        If both server and client modes are enabled, the function prints an error message and exits.
        If the provided port is not within the valid range [1024, 65535], it prints an error message and exits.
        If the provided IP address is invalid, it prints an error message and exits.
        If a file is provided and it's not a .jpg file, it prints an error message and exits.
        If neither server nor client mode is enabled, it prints an error message and exits.
    """
def main():
    # Create a parser object to handle command-line arguments
    # Add arguments to the parser
    # These arguments will allow the user to specify whether to run as a client or server, 
    # the server IP, file to transfer, server port, window size, and sequence number to discard
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--client", action="store_true", help="Run as client.")
    parser.add_argument("-s", "--server", action="store_true", help="Run as server.")
    parser.add_argument('-i', '--ip', type=str, default="127.0.0.1", help='Server IP address.')
    parser.add_argument("-f", "--file", type=str, help="File to transfer.")
    parser.add_argument('-p', '--port', default=8088, type=int, help='Server port number.')
    parser.add_argument('-w', '--window', default=3, type=int, help="The window size")
    parser.add_argument('-d', '--discard', type=int, help="Value of seq to skip")
    args = parser.parse_args()

    # Check if both server and client modes are enabled, print an error message and exit if true
    if args.server and args.client:
        print('You cannot run server and client at the same time')
        exit(1)

    # Check if the provided port is within the valid range. If not, print an error message and exit
    if not 1024 <= args.port <= 65535:
        print('Invalid port. It must be within the range [1024,65535]')
        exit(1)

    # Validate the provided IP address. If it's not valid, print an error message and exit
    if not re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', args.ip) or not all(0 <= int(part) <= 255 for part in args.ip.split('.')):
        print('Invalid IP. It should be in this format: 10.1.2.3 and each block must be in the range [0,255]')
        exit(1)

     # Check if a file is provided and if it's a .jpg file. If not, print an error message and return
    if args.file is not None and not re.match(r'.*\.jpe?g$', args.file):
        print("Invalid file, must be a .jpg file.")
        return
    # Run in server mode if the server argument is enabled
    if args.server:
        server(args)
    # Run in client mode if the client argument is enabled
    elif args.client:
        client(args)
    # If neither mode is enabled, print an error message and exit
    else:
        print('You must run either in server or client mode')
        exit(1)
        
# Call the main function when the script is run
if __name__ == "__main__":
    main()