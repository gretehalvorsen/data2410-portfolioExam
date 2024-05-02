from server import server
from client import client
import argparse


parser = argparse.ArgumentParser(description='File Transfer Application')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-s', '--server', action='store_true')
group.add_argument('-c', '--client', action='store_true')
parser.add_argument('-f', '--file', help='Filename')
parser.add_argument('-i', '--ip', help='IP adress')

if args.server:
    server()
elif args.client:
    client()
