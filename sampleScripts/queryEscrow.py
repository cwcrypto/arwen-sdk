import argparse
import os
import sys

sys.path.append("../")
import arwenlib.ArwenClient as arwen
import arwenlib.supportFunctions as sf
from arwenlib import constants as c

from arwenlib import startArwenClient

# reseveAddress, blockchain, exchId, expireTime, qty

parser = argparse.ArgumentParser(prog='makeTrade', description='creates a trade')

# Add the arguments
parser.add_argument('--id',
    '-i',
    type=str,
    required=True,
    help='Id of user escrow you find')

parser.add_argument('--type',
    '-t',
    type=str,
    required=True,
    help='type of escrow you want to find (USER or EXCH)')

# Execute the parse_args() method
args = parser.parse_args()

client = startArwenClient()

config = c.ArwenConfig()
configFilePath = '../config.json'
config.loadConfig(configFilePath)

escrow = client.getEscrowById(sf.EscrowType(args.type), args.id)

print(escrow.toString())