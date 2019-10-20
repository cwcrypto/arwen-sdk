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
parser.add_argument('--userEscrowId',
    '-u',
    type=str,
    required=True,
    help='Id of user escrow you want to sell from')

parser.add_argument('--exchEscrowId',
    '-e',
    type=str,
    required=True,
    help='Id of exchange escrow you want to buy from')

parser.add_argument('--qty',
    '-q',
    type=str,
    required=True,
    help='amount to trade')

parser.add_argument('--side',
    '-s',
    type=str,
    required=True,
    help='BUY or SELL')

# Execute the parse_args() method
args = parser.parse_args()

client = startArwenClient()

config = c.ArwenConfig()
configFilePath = '../config.json'
config.loadConfig(configFilePath)

client.registerApiKeys(config.testnetApiKey, config.testnetApiSecret, sf.Exchange.BINONCE)

userEscrow = client.queryEscrowById(sf.EscrowType.USER, args.userEscrowId)
exchEscrow = client.queryEscrowById(sf.EscrowType.EXCH, args.exchEscrowId)

side = sf.Side(args.side)
order = None

if(side == sf.Side.BUY):
    order = client.newBuyOrder(userEscrow, exchEscrow, args.qty)
else:
    order = client.newSellOrder(userEscrow, exchEscrow, args.qty)

print(f'OrderId: {order.orderId}')