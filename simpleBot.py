import requests
import json
import math
import pprint

import supportFunctions as sf
import userEscrow
import exchEscrow
import orders

import constants as c


def initArwenClient():
    return requests.post(f'{c.url}/init')

def pingArwenClient():
    return requests.get(f'{c.url}/ping')

def timeArwenClient():
    return requests.get(f'{c.url}/time')

def cleanupBadEscrows():
    
    endpoint = '/cleanup'
    
    return sf.sendRequest(c.url, endpoint)

def exchanges():

    endpoint = '/exchanges'

    return sf.sendRequest(c.url, endpoint)

def registerApiKeys():

    endpoint = '/register'

    regParams = dict()
    regParams['exchId'] = 'Binonce'
    regParams['apiKey'] = c.testnetApiKey
    regParams['apiSecret'] = c.testnetApiSecret

    return sf.sendRequest(c.url, endpoint, regParams)


if __name__ == "__main__":
    resp = initArwenClient()
    print(resp.text)
    time = timeArwenClient()
    print(time.text)

    # exchInfo = exchanges()
    # pprint.pprint(exchInfo)

    register = registerApiKeys()
    # pprint.pprint(register)

    newUE = userEscrow.createNewUserEscrow()
    print('User Escrow (Unfunded)')
    print(f'userEscrowId:    {newUE.userEscrowId}')
    print(f'address to fund: {newUE.escrowAddress}')
    print(f'amount to fund:  {newUE.amountToFund}')


    input(f'Please fund userEscrow before pressing any key')

    print('All user escrows that are not closed:')
    queryUE = userEscrow.queryUserEscrows()
    pprint.pprint(queryUE)

    newEE = exchEscrow.createNewExchEscrow(userEscrow=newUE)
    print('Exchage Escrow (Funded by Exchage Automatically)')
    print(f'exchEscrowId:    {newEE.exchEscrowId}')
    print(f'escrow ddress:   {newEE.escrowAddress}')
    print(f'pricePaid:       {newEE.pricePaid}')

    input(f'Please wait for exchEscrow to confirm on blockchain before pressing any key')

    print('Creating a sell order of 0.01 BTC for LTC')

    # You can use the Lite escrows if you know the escrowId and currency
    ue = userEscrow.userEscrowLite(newUE.userEscrowId, sf.Blockchain.BTC)
    ee = exchEscrow.exchEscrowLite(newEE.exchEscrowId, sf.Blockchain.LTC)

    order = orders.sellTrade(ue, ee, 0.001)
    print('Order Details:')
    pprint.pprint(order)

    input(f'press key to send execute order')

    execute = orders.execute(order)
    print(f'Order Execution: {execute}')

    details = userEscrow.queryUserEscrows(ue.userEscrowId)
    print('Updated user Escrow details, notice the trade made')
    pprint.pprint(details)

    resp = cleanupBadEscrows()
    pprint.pprint(resp)
