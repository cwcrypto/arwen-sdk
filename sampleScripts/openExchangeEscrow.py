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

parser.add_argument('--exchId',
    '-e',
    type=str,
    required=True,
    help='exchange to trade with')

parser.add_argument('--quantity',
    '-q',
    type=float,
    required=True,
    help='size of escrow in currency units')

parser.add_argument('--expiryTime',
    '-t',
    type=float,
    required=True,
    help='how long to keep the escrow open in days (float)')

parser.add_argument('--userEscrowId',
    '-u',
    type=str,
    required=True,
    help='user escrow to pay the escrow fee with')

# Execute the parse_args() method
args = parser.parse_args()

client = startArwenClient()

config = c.ArwenConfig()
configFilePath = '../config.json'
config.loadConfig(configFilePath)

newEE = client.createNewExchEscrow(
    reserveAddress=args.resvAddr,
    userEscrowId=args.userEscrowId,
    exchId=sf.Exchange(args.exchId),
    exchEscrowCurrency=sf.Blockchain(args.blockchain),
    expiryTime=sf.generateEscrowTimelock(args.expiryTime),
    amount=args.quantity)

print(f'escrowId:           {newEE.escrowId}')
print(f'fudingAddress:      {newEE.escrowAddress}')
print(f'amountToFund:       {newEE.escrowFeePaid}')

sf.waitForEscowToOpen(newEE, client)

print('Escrow opened successfully')