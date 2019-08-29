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

    # url = client.getOAuthUrl('kucoinrfq')['oauthUrl']
    
    # print('Please copy-paste the following URL into your browser')
    # print('You will be shown a KuCoin OAuth page, log in ')
    # print(url)

    # exchInfo = client.exchanges()
    # pprint.pprint(exchInfo)

    register = client.registerApiKeys(apiKey=c.testnetApiKey, apiSecret=c.testnetApiSecret)
    pprint.pprint(register)

    print(c.testnetBTC)

    newUE = client.createNewUserEscrow(reserveAddress=c.testnetBTC)
    print('User Escrow (Unfunded)')
    print(f'userEscrowId:    {newUE.escrowId}')
    print(f'address to fund: {newUE.escrowAddress}')
    print(f'amount to fund:  {newUE.amountToFund}')

    print('tradeBot will wait until escrow has been funded and confirmed by user')
    sf.waitForEscowToOpen(newUE, client)

    print('All user escrows that are not closed:')
    queryUE = client.queryEscrows(escrowType=sf.EscrowType.USER)
    pprint.pprint(queryUE)

    newEE = client.createNewExchEscrow(reserveAddress=c.testnetLTC, userEscrow=newUE)
    print('Exchage Escrow (Funded by Exchage Automatically)')
    print(f'exchEscrowId:    {newEE.escrowId}')
    print(f'escrow address:  {newEE.escrowAddress}')
    print(f'pricePaid:       {newEE.pricePaid}')

    print('tradeBot will wait until escrow has been funded and confirmed by exchange')
    sf.waitForEscowToOpen(newEE, client)

    print('All exch escrows that are not closed:')
    queryEE = client.queryEscrows(escrowType=sf.EscrowType.EXCH)
    pprint.pprint(queryEE)

    print('Hooray! You have set up a user and exchange escrow!')
    print('Write down your user and exchange escrowId and try the simpleBot script!')