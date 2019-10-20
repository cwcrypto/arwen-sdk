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
    help='Id of user escrow you find')

parser.add_argument('--type',
    '-t',
    type=str,
    required=True,
    help='type of escrow you want to find (USER or EXCH)')

parser.add_argument('--open',
    '-o',
    type=bool,
    required=False,
    default=False,
    help='if you want to filter for open or closed escrows')

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

escrow = None

if(args.id != None):
    escrow = client.queryEscrowById(sf.EscrowType(args.type), args.id)
    print(escrow.toString())
else:
    escrow = client.queryEscrows(sf.EscrowType(args.type), isOpen=args.open, limit=args.limit, fromTime=args.startTime)
    print(escrow)