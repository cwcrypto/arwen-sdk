import argparse
import os
import sys

sys.path.append("../")
import arwenlib.ArwenClient as arwen
import arwenlib.supportFunctions as sf
from arwenlib import constants as c

from arwenlib import startArwenClient

print('ONLY USED FOR TESTNET EXCHANGES')

parser = argparse.ArgumentParser(prog='registerApiKeys', description='Register API keys for a particular exchange, please make sure your keys are in config.json')

parser.add_argument('--exchid',
    '-e',
    type=str,
    required=True,
    help='What exchange to register for')

args = parser.parse_args()

client = startArwenClient()
config = c.ArwenConfig()
config.loadConfig('../config.json')

regStatus = client.registerApiKeys(apiKey=config.testnetApiKey, apiSecret=config.testnetApiSecret, exchId=sf.Exchange(args.exchid))

print(regStatus)
