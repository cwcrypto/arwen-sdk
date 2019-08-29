import requests
import json
import math
import pprint

from arwenlib import ArwenClient as Arwen
from arwenlib import baseEscrowDetails as baseDetails
from arwenlib import supportFunctions as sf

from arwenlib import startArwenClient

import constants

if __name__ == "__main__":
    c = constants.ArwenConfig()
    c.loadConfig()
    
    client = startArwenClient(ip=c.ip, port=c.port)

    client.registerApiKeys(c.testnetApiKey, c.testnetApiSecret)

    print('Registering API Key and Secret for testnet Binonce')
    register = client.registerApiKeys(apiKey=c.testnetApiKey, apiSecret=c.testnetApiSecret, exchId=sf.Exchange.BINONCE)
    pprint.pprint(register)

    print('Creating a new user escrow with the following parameters')
    print(f'Reserve address:    {c.testnetBTC}')
    print(f'exchId:             {sf.Exchange.BINONCE}')
    print(f'currency            {sf.Blockchain.BTC.value}')
    print(f'expire time:        {sf.generateEscrowTimelock(2.0)} // 2 days from now')
    print(f'qty:                {0.025}\n')

    newUE = client.createNewUserEscrow(reserveAddress=c.testnetBTC)
    print('User Escrow (Unfunded)')
    print(f'userEscrowId:           {newUE.escrowId}')
    print(f'escrow address to fund: {newUE.escrowAddress}')
    print(f'amount to fund:         {newUE.amountToFund} {newUE.currency}')

    print('tradeBot will wait until escrow has been funded and confirmed by user')
    sf.waitForEscowToOpen(newUE, client)

    print('All user escrows that are not closed:')
    queryUE = client.queryEscrows(escrowType=sf.EscrowType.USER)
    pprint.pprint(queryUE)


    print('Creating a new exchange escrow with the following parameters')
    print(f'Reserve address:    {c.testnetLTC}')
    print(f'exchId:             {sf.Exchange.BINONCE}')
    print(f'currency            {sf.Blockchain.LTC.value}')
    print(f'expire time:        {sf.generateEscrowTimelock(2.0)} // 2 days from now')
    print(f'qty:                2.0\n')

    newEELtc = client.createNewExchEscrow(reserveAddress=c.testnetLTC, userEscrow=newUE, exchEscrowCurrency=sf.Blockchain.LTC, qty=2.0)
    print('Exchage Escrow (Funded by Exchage Automatically)')
    print(f'exchEscrowId:           {newEELtc.escrowId}')
    print(f'funded escrow address:  {newEELtc.escrowAddress}')
    print(f'pricePaid:              {newEELtc.pricePaid} {newUE.currency}')

    print('tradeBot will wait until escrow has been funded and confirmed by exchange')
    sf.waitForEscowToOpen(newEELtc, client)

    print('Creating a new exchange escrow with the following parameters')
    print(f'Reserve address:    {c.testnetBCH}')
    print(f'exchId:             {sf.Exchange.BINONCE}')
    print(f'currency            {sf.Blockchain.BCH.value}')
    print(f'expire time:        {sf.generateEscrowTimelock(2.0)} // 2 days from now')
    print(f'qty:                0.5\n')


    newEEBch = client.createNewExchEscrow(reserveAddress=c.testnetBCH, userEscrow=newUE,exchEscrowCurrency=sf.Blockchain.BCH, qty=0.5)
    print('Exchage Escrow (Funded by Exchage Automatically)')
    print(f'exchEscrowId:           {newEEBch.escrowId}')
    print(f'funded escrow address:  {newEEBch.escrowAddress}')
    print(f'pricePaid:              {newEEBch.pricePaid} {newUE.currency}')

    print('tradeBot will wait until escrow has been funded and confirmed by exchange')
    sf.waitForEscowToOpen(newEEBch, client)

    print('All exch escrows that are not closed:')
    queryEE = client.queryEscrows(escrowType=sf.EscrowType.EXCH)
    pprint.pprint(queryEE)

    print(f'Hooray! You have set up a user (escrowId {newUE.escrowId}) and exchange (escrowId {newEELtc.escrowId}) escrow!')
    print('Write down your user and exchange escrowId and try the simpleTrade script!')