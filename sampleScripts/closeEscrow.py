import argparse
import os
import sys

sys.path.append("../")
import arwenlib.ArwenClient as arwen
import arwenlib.supportFunctions as sf
from arwenlib import constants as c

from arwenlib import startArwenClient

# reseveAddress, blockchain, exchId, expireTime, qty

parser = argparse.ArgumentParser(prog='openUserEscrow', description='Open a user escrow')

# Add the arguments
parser.add_argument('--type',
    '-t',
    type=str,
    required=True,
    help='USER or EXCH')

parser.add_argument('--id',
    '-i',
    type=str,
    required=True,
    help='escrowId to close')


args = parser.parse_args()

client = startArwenClient()

config = c.ArwenConfig()
configFilePath = '../config.json'
config.loadConfig(configFilePath)

userEscrow = client.getEscrowById(sf.EscrowType.USER, args.userEscrowId)

resp = None

if(sf.EscrowType(args.type) == sf.EscrowType.USER):
    resp = client.closeUserEscrowById(args.id)
else:
    resp = client.closeExchEscrowById(args.id)

print(resp)
