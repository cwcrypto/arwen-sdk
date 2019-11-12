import argparse
import os
import sys

sys.path.append("../")
import arwenlib.ArwenClient as arwen
import arwenlib.supportFunctions as sf
from arwenlib import constants as c

from arwenlib import startArwenClient

parser = argparse.ArgumentParser(prog='executeTrade', description='Executes a trade')

# Add the arguments
parser.add_argument('--id',
    '-i',
    type=str,
    required=True,
    help='Id of the trade you want to execute')

args = parser.parse_args()

client = startArwenClient()

config = c.ArwenConfig()
configFilePath = '../config.json'
config.loadConfig(configFilePath)

execute = client.executeById(args.id)
print(f'executed: {execute}')

order = client.queryOrdersById(args.id)
print(order)