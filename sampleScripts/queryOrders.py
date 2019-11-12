import argparse
import os
import sys

sys.path.append("../")
import arwenlib.ArwenClient as arwen
import arwenlib.supportFunctions as sf
from arwenlib import constants as c

from arwenlib import startArwenClient

# reseveAddress, blockchain, exchId, expireTime, qty

parser = argparse.ArgumentParser(prog='queryEscrow', description='query for escrows, optionally query with an id for a particular escrow')

# Add the arguments
parser.add_argument('--id',
    '-i',
    type=str,
    required=False,
    default=None,
    help='orderId you are looking for')

parser.add_argument('--exchId',
    '-e',
    type=str,
    required=False,
    default=None,
    help='the exchange you placed the order at')

parser.add_argument('--open',
    '-o',
    type=bool,
    required=False,
    default=True,
    help='if you want to filter for open or closed orders')

parser.add_argument('--limit',
    '-l',
    type=int,
    required=False,
    default=1000,
    help='how many results to see')

parser.add_argument('--startTime',
    '-s',
    type=int,
    required=False,
    default=None,
    help='timestamp to filter from')

# Execute the parse_args() method
args = parser.parse_args()

client = startArwenClient()

config = c.ArwenConfig()
configFilePath = '../config.json'
config.loadConfig(configFilePath)

if(args.id != None):
    order = client.queryOrdersById(orderId=args.id)

    if(order == None):
        print('No orders fit your query')
        exit(0)
    else:
        print(order)

else:
    order = client.queryOrders(exchId=args.exchId, isFinal=args.open, limit=args.limit, fromTime=args.startTime)

    if(order == None):
        print('No orders fit your query')
        exit(0)
    else:
        [print(f'======================\n{o}') for o in order]
