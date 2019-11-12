import argparse
import os
import sys

sys.path.append("../")
import arwenlib.ArwenClient as arwen
import arwenlib.supportFunctions as sf
from arwenlib import constants as c

from arwenlib import startArwenClient

# reseveAddress, blockchain, exchId, expireTime, qty

parser = argparse.ArgumentParser(prog='cancelTrade', description='Cancels a trade')

# Add the arguments
parser.add_argument('--id',
    '-i',
    type=str,
    required=True,
    help='Id of user escrow you find')

# Execute the parse_args() method
args = parser.parse_args()

client = startArwenClient()

config = c.ArwenConfig()
configFilePath = '../config.json'
config.loadConfig(configFilePath)

cancel = client.cancelById(args.id)
print(f'canceled: {cancel}')

order = client.queryOrdersById(args.id)
print(order)

