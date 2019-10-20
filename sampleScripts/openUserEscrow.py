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
parser.add_argument('--resvAddr',
    '-r',
    type=str,
    required=True,
    help='address to send funds to when escrow closes')

parser.add_argument('--blockchain',
    '-b',
    type=str,
    required=True,
    help='currency to open an escrow in')

parser.add_argument('--exchid',
    '-e',
    type=str,
    required=True,
    help='exchange to trade with')

parser.add_argument('--quantity',
    '-q',
    type=float,
    required=True,
    help='size of escrow in currency units')

parser.add_argument('--expirytime',
    '-t',
    type=float,
    required=True,
    help='how long to keep the escrow open in days (float)')

# Execute the parse_args() method
args = parser.parse_args()

client = startArwenClient()

config = c.ArwenConfig()
configFilePath = '../config.json'
config.loadConfig(configFilePath)

newUE = client.createNewUserEscrow(
    reserveAddress=args.resvAddr,
    exchId=sf.Exchange(args.exchid),
    currency=sf.Blockchain(args.blockchain),
    expiryTime=sf.generateEscrowTimelock(args.expirytime),
    amount=args.quantity)

print(f'escrowId:           {newUE.escrowId}')
print(f'fudingAddress:      {newUE.escrowAddress}')
print(f'amountToFund:       {newUE.amountToFund}')

sf.waitForEscowToOpen(newUE, client)

print('Escrow opened successfully')